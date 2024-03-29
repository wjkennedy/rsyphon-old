package Boot::YaBoot;

#   $Header$

#   Copyright (c) 2001 International Business Machines

#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
 
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
 
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#   Donghwa John Kim <johkim@us.ibm.com>

=head1 NAME

Boot::YaBoot - YaBoot bootloader configuration module.

=head1 SYNOPSIS

  my $bootloader = new Boot::YaBoot(%bootvars);

  if($bootloader->footprint_loader()) {
      $bootloader->install_config();
  }
  
  if($bootloader->footprint_config() && $bootloader->footprint_loader()) {
    $boot->install_loader();
  }

  my @fileschanged = $bootloader->files();

=cut

use strict;
use Carp;
use vars qw($VERSION);
use Boot;
use Util::Cmd qw(:all);
use Util::Log qw(:print);

$VERSION = sprintf("%d", q$Revision: 668 $ =~ /(\d+)/);

push @Boot::boottypes, qw(Boot::YaBoot);

sub new {
    my $class = shift;
    my %this = (
                root => "",
                filesmod => [],
		boot_bootdev => "", ### device to which Yaboot will be installed
		boot_timeout => 50,
                boot_rootdev => "",
                @_,
		default_root => "",
                bootloader_exe => "",
		platform_t => "",    ### platform type identifier
               );

    $this{config_file} = "$this{root}" . "/etc/yaboot.conf";

    ### a PPC hardware?
    if (open(PROC,"<$this{root}/proc/cpuinfo")) {
        while(<PROC>) {
            if(/^machine.*chrp/i) {  ### We only support CHRP (IBM RS/6000) now.
                $this{platform_t} = "chrp";
                last;
            }
        }
        close(PROC);
	# Let us see if we can find a yaboot image.
        
        if ($this{platform_t}) {
            if(-e $this{root}. "/boot/yaboot.". $this{platform_t}) {
                $this{bootloader_exe} = "$this{root}/boot/yaboot.$this{platform_t}";
            } elsif (-e $this{root}."/boot/yaboot") {
                $this{bootloader_exe} = "$this{root}/boot/yaboot";
            } elsif (-e $this{root}."/usr/lib/yaboot/yaboot") {
                $this{bootloader_exe} = "$this{root}/usr/lib/yaboot/yaboot";
            } else {
                verbose("Read README file for naming of Yaboot image.");
                carp("Cannot find a Yaboot image.\n");
            }
        }
        verbose("YaBoot executable is set to: $this{bootloader_exe}."); 
    } else {
        ### Cannot open /proc/cpuinfo
        verbose("Error opening $this{root}/proc/cpuinfo.");
        verbose("If a PPC machine, be sure to have $this{root}/proc/cpuinfo readable.");
        verbose("Cannot open $this{root}/proc/cpuinfo.\n");
    }
    bless \%this, $class;
}

=head1 METHODS

The following methods exist in this module:

=over 4

=item files()

The files() method is merely an accessor method for the all files
touched by the instance during its run.

=cut

sub files {
    my $this = shift;
    return @{$this->{filesmod}};
}

=item footprint_loader()

This method returns "TRUE" if executable YaBoot bootloader is installed. 

=cut

sub footprint_loader {
    my $this = shift;
    return $this->{bootloader_exe};
}

=item footprint_config()

This method returns "TRUE" if YaBoot config file, i.e. "/etc/yaboot.conf", exists. 

=cut

sub footprint_config {
    my $this = shift;
    return -e $this->{config_file};
}

=item install_config()

This method reads the System Configurator's config file and creates YaBoot's 
config file, i.e. "/etc/yaboot.conf".

=cut

sub install_config {
    my $this = shift;

    if(!$this->{boot_bootdev})
    {
        croak("Error: BOOTDEV must be specified.\n");
    }
    if(!$this->{boot_defaultboot}) 
    {
        croak("Error: DEFAULTBOOT must be specified.\n");
    }

    my $file = $this->{root} . "/etc/yaboot.conf";
    open(OUT,">$file") or croak("Couldn\'t open $file for writing");
    
    print OUT "##################################################\n";
    print OUT "# This file is generated by System Configurator. #\n";
    print OUT "##################################################\n";
    print OUT "\n";
    
    print OUT "#----- Global Options -----#\n";
    
    ### Specify the root device.
    if ($this->{boot_rootdev}) {
	print OUT "# Device to be mounted as the root ('/') \n";
	print OUT "root=" . $this->{boot_rootdev} . "\n";
    }
    
    ### timeout
    if ($this->{boot_timeout}) {
	print OUT "# The number of deciseconds (0.1 seconds) to wait before booting. \n";
	print OUT "prompt\n";
	print OUT "timeout=" . $this->{boot_timeout} . "\n";
    }
    
    ### default kernel image to boot with
    unless ($this->{boot_defaultboot}) {
	croak("Error: default kernel image not specified.");
    }
    print OUT "# The default kernel image to boot. \n";
    print OUT "default=" . $this->{boot_defaultboot} . "\n";
    
    ### Options to append at boot time
    if ($this->{boot_append})
    {
	print OUT "# Kernel command line options. \n";
	print OUT "append=" . $this->{boot_append} . "\n";
    }    
    
    print OUT "\n";
    
    foreach my $key (sort keys %$this) {
	if ($key =~ /^(kernel\d+)_path/) {
	    $this->setup_kernel($1,\*OUT);
	}
    }
    
    close(OUT);
    
    push @{$this->{filesmod}}, "$file";

    ### Indicate that Yaboot has been successfully installed.
    1;
}

=item setup_kernel()

An internal method.
This method sets up a kernel image as specified in the config file.

=cut

sub setup_kernel {
    my ($this, $image, $outfh) = @_;
    
    ### If we cannot derive root device for the default boot image, croak.
    if ($this->{boot_defaultboot} eq $this->{$image . "_label"}) {
        unless ($this->{boot_rootdev} || $this->{$image . "_rootdev"}) {
            croak("ROOTDEV cannot be derived for the default boot image.\n");
	}
    }
    
    print $outfh "#----- Options for \U$image -----#\n";
    ### path to the kernel image 
    print $outfh "### Kernel image \n";
    print $outfh "image=" . $this->{root} . $this->{$image . "_path"} . "\n";

    ### label
    print $outfh "### Label for $image \n";
    print $outfh "label=" . $this->{$image . "_label"} . "\n";

    print $outfh "read-only\n";

    ### Check for command line kernel options. 
    if ($this->{$image. "_append"}) {
        print $outfh "### Kernel command line options \n";
        print $outfh "append=" . "\"" . $this->{$image . "_append"} . "\"" . "\n";
    }    
    
    ### Override global rootdev option?
    if ($this->{$image. "_rootdev"}) {
        print $outfh "### Device to be mounted as the root ('/') \n";
        print $outfh "root=" . $this->{$image . "_rootdev"} . "\n";
    }    
    
    ### Initrd image
    if ($this->{$image. "_initrd"}) {
        print $outfh "### initrd \n";
        print $outfh "initrd=" . $this->{root} . $this->{$image . "_initrd"} . "\n";
    }        
    
    print $outfh "\n";
}

sub install_loader {
    my $this = shift;
    my $bdevice;

    my $fdiskpath = which("fdisk");
    chomp($fdiskpath);
    if (!$fdiskpath) {
	croak("Error: fdisk utility not found on the system.\n");
    }
 
    if ($this->{boot_bootdev}) {
        $bdevice = $this->{boot_bootdev}; # extracting the device part
    }
    else {
	# We will go through all the devices and write Yaboot image
	# to every PREP parition. 
	$bdevice = find_bootdev();
    }

    my $preppart = find_prep_partition($bdevice);
    if(!$preppart) {
        croak("Error: PReP partition not defined, can't continue");
    }

    ### Now, let's copy the boot image to the boot partition. 
    my $ddpath = which("dd");
    chomp($ddpath);
    if (!$ddpath) {
        croak("Error: dd utility not found on the system.\n");
    }
    
    my $cmd = "$ddpath if=$this->{bootloader_exe} of=$preppart 2>&1";
    verbose("Running $cmd");

    my $ddoutput = qx($cmd);
    my $exitval = $? >> 8;
    if ($exitval) {
        croak("$ddoutput\n");
    }
    
    1; 
}

# the following 2 functions come from the iSeries.pm module.  Need
# to think about consolodating ppc code at some point

sub find_prep_partition {
    my $dev = shift;
    my $part = "";
    verbose("Scanning $dev for prep boot partitions");
    if(open(FDISK, "fdisk -l $dev |")) { 
        while(<FDISK>) {
            s/\*//;
            if(/^(\/dev\/\S+)\s+\S+\s+\S+\s+\S+\s+(\w\w)\s+/) {
                debug("$1 has type $2");
                if($2 eq "41") {
                    $part = $1;
                    verbose("Found prep partition for device $2");
                    last;
                }
            }
        }
        close(FDISK);
    } else {
        carp ("Couldn't run 'fdisk -l $dev |'");
    }
    return $part;
}

sub find_bootdev {
    verbose("Attempting to find bootdevice based on partition scan");
    my @possible = ();
    opendir(DEV,"/dev");
    while(my $dev = readdir(DEV)) {
        if($dev =~ /^[hs]d\w$/) {
            verbose("Adding $dev to the list of possible boot devices");
            push @possible, "/dev/$dev";
        }
    }
    closedir(DEV);
    
    foreach my $dev (@possible) {
        verbose("Looking for prep partitions on $dev");
        my $part = find_prep_partition($dev);
        if($part) {
            return $dev;
        }
    }
}

=back

=head1 AUTHOR

  Donghwa John Kim <donghwajohnkim@yahoo.com>

=head1 SEE ALSO

L<SystemConifg::Boot>, L<perl>

=cut

1;




















