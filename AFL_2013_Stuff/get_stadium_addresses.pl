#!/usr/bin/perl

use warnings;
use strict;
use lib '/Users/alexlovejoy/perl/lib/';
use LWP::Simple;
use HTML::Scrubber;

my $scrubber = HTML::Scrubber->new( allow => [ qw[ p b i u hr br ] ] );

#Get the html code for the list of MLB stadium addresses
my $html = get('http://mlb.mlb.com/team/');

#Convert the html code to something reasonable
$scrubber->deny( qw[ p bp i u hr br ] );

#Print it
print $scrubber->scrub($html);
