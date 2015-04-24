package Boot::Kboot;

#   $Header$

#   Copyright (c) 2007 Erich Focht <efocht@hpce.nec.com>
#                      All rights reserved.

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


=head1 NAME

Boot::Kboot - Kboot bootloader configuration module.

=head1 SYNOPSIS

  my $bootloader = new Boot::Kboot(%bootvars);

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

$VERSION = sprintf("%d", q$Revision: 698 $ =~ /(\d+)/);

push @Boot::boottypes, qw(Boot::Kboot);

sub new {
    my $class = shift;
    my %this = (
                root => "",
                filesmod => [],
		boot_bootdev => "", ### device to which Kboot will be installed
		boot_timeout => 50,
                boot_rootdev => "",
                @_,
		default_root => "",
                bootloader_exe => "",
		platform_t => "",    ### platform type identifier
               );

    $this{config_file} = "$this{root}" . "/etc/kboot.conf";

    ### a PPC hardware?
    if (open(PROC,"<$this{root}/proc/cpuinfo")) {
        while(<PROC>) {
            if(/^platform.*PS3/i) {  ### We only support PS3 now.
                $this{platform_t} = "ps3";
                last;
            }
        }
        close(PROC);
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

This method returns "TRUE" if a kboot.conf file is available.

=cut

sub footprint_loader {
    my $this = shift;
    return (($this->{platform_t}) && (-x $this->{config_file}));
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
    my $extra1 = $this->{boot_extras};
    my $extra2 = $this->{boot_extras2};
    my $extra3 = $this->{boot_extras3};

    if(!$this->{boot_bootdev})
    {
        croak("Error: BOOTDEV must be specified.\n");
    }
    if(!$this->{boot_defaultboot}) 
    {
        croak("Error: DEFAULTBOOT must be specified.\n");
    }

    my $file = $this->{root} . "/etc/kboot.conf";
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
	print OUT "# The number of seconds to wait before booting. \n";
	print OUT "timeout=" . $this->{boot_timeout}/10 . "\n";
    }
    
    ### default kernel image to boot with
    unless ($this->{boot_defaultboot}) {
	croak("Error: default kernel image not specified.");
    }
    print OUT "# The default kernel image to boot. \n";
    print OUT "default=" . $this->{boot_defaultboot} . "\n";
    
    print OUT "$extra1\n" if $extra1 ne "";
    print OUT "$extra2\n" if $extra2 ne "";
    print OUT "$extra3\n" if $extra3 ne "";
    print OUT "\n";
    
    foreach my $key (sort keys %$this) {
	if ($key =~ /^(kernel\d+)_path/) {
	    $this->setup_kernel($1,\*OUT);
	}
    }
    
    close(OUT);
    
    push @{$this->{filesmod}}, "$file";

    ### Indicate that kboot has been successfully installed.
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

    print $outfh "#------ $image --------#\n";
    print $outfh $this->{$image . "_label"} . "='" .
	$this->{$image . "_path"} . " ";
    ### Initrd image
    if ($this->{$image. "_initrd"}) {
        print $outfh "initrd=" . $this->{$image."_initrd"}." ";
    }
    if ($this->{$image. "_append"}) {
        print $outfh $this->{$image."_append"} . " ";
    }
    if ($this->{boot_append}) {
	print $outfh $this->{boot_append} . " ";
    }
    ### Override global rootdev option?
    if ($this->{$image."_rootdev"} &&
	($this->{$image."_rootdev"} ne $this->{boot_rootdev})) {
        print $outfh "root=" . $this->{$image."_rootdev"} . " ro ";
    }
    print $outfh "init=/sbin/init'\n";
}

sub install_loader {
    my $this = shift;
    1; 
}

=back

=head1 AUTHOR

  Erich Focht <efocht@hpce.nec.com>

=head1 SEE ALSO

L<SystemConfig::Boot>, L<perl>

=cut

1;

