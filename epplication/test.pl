#!/usr/bin/env perl
use 5.018;
use warnings;

use FindBin qw/$Bin/;
use lib "$Bin/lib";
use EPPlication::CLI;

my $host   = 'http://localhost';
my $port   = 80;
my $user   = 'admin';
my $pass   = 'admin123';
my $branch = 'master';
my $config = 'do-config';
my $test   = 'test portal';

my $cli = EPPlication::CLI->new( host => $host, port => $port );
$cli->login( $user, $pass );

my $branch_id = $cli->get_branch_id_by_name('master');
my $config_id = $cli->get_test_id_by_name( $config, $branch_id );
my $test_id   = $cli->get_test_id_by_name( $test, $branch_id );

my $job_id = $cli->create_job({
    test_id   => $test_id,
    config_id => $config_id,
});

say "test details -> http://localhost:8080/job/$job_id/show (admin/admin123)";
say 'selenium browser -> `xtightvncviewer localhost::5900` (password: `secret`)';

my $status = '';
while ($status ne 'finished') {
    my $job = $cli->get_job($job_id);
    $status = $job->{status};
    if ($status eq 'finished') {
        say 'job finished.';
        say 'duration: ' . $job->{summary}{duration} . ' seconds.';
        if (defined $job->{summary}{errors}) {
            say 'errors ' . $job->{summary}{errors} . '.';
        }
        else {
            say 'no errors.';
        }
    }
    else {
        say $status;
        sleep 10;
    }
}
