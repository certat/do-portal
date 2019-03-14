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

say "job started: http://localhost:8080/job/$job_id/show";
say 'if you want to watch the selenium browser -> `xtightvncviewer localhost::5900` (password: `secret`)'
