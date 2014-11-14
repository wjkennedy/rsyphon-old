#
# "rsyphon"

package rsyphon::Config;

use strict;
use AppConfig;

BEGIN {
    use Exporter();

    @rsyphon::Config::ISA       = qw(Exporter);
    @rsyphon::Config::EXPORT    = qw();
    @rsyphon::Config::EXPORT_OK = qw($config);

}
use vars qw($config);

$config = AppConfig->new(
    'default_image_dir'         => { ARGCOUNT => 1 },
    'default_override_dir'      => { ARGCOUNT => 1 },
    'autoinstall_script_dir'    => { ARGCOUNT => 1 },
    'autoinstall_boot_dir'      => { ARGCOUNT => 1 },
    'rsyncd_conf'               => { ARGCOUNT => 1 },
    'rsync_stub_dir'            => { ARGCOUNT => 1 },
    'tftp_dir'                  => { ARGCOUNT => 1 },
    'net_boot_default'          => { ARGCOUNT => 1 },
    'autoinstall_tarball_dir'   => { ARGCOUNT => 1 },
    'autoinstall_torrent_dir'   => { ARGCOUNT => 1 },
);

my $config_file = '/etc/rsyphon/rsyphon.conf';
$config->file($config_file) if (-f $config_file);

$::main::config = $config;

1;
