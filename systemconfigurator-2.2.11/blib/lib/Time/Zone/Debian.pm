package Time::Zone::Debian;

#   $Id: Debian.pm 664 2007-01-15 21:40:36Z arighi $

#   Copyright (c) 2002 International Business Machines

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

#   Sean Dague <sean@dague.net>

use strict;
use Carp;
use Data::Dumper;
use base qw(Time::Zone::Generic);
use vars qw($VERSION);
use Util::FileMod;

$VERSION = sprintf("%d", q$Revision: 664 $ =~ /(\d+)/);

push @Time::Zone::tztypes, qw(Time::Zone::Debian);

sub footprint {
    my $this = shift;
    $this->{_conf_file} = $this->chroot("/etc/timezone");
    
    if(-e $this->conf_file) {
        return 1;
    }
    return undef;
}

sub setup {
    my $this = shift;

    my $file = $this->conf_file;
    open(OUT,">$file") or return undef;
    print OUT $this->zone, "\n";
    close(OUT);
    
    $this->files($this->conf_file);

}

1;
