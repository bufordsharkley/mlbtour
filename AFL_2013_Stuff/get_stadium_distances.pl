#!/usr/bin/perl

use warnings;
use strict;
use lib '/Users/alexlovejoy/perl/lib/';
use LWP::Simple;

#######################################################
#Takes in a file with team names and addresses of the format:
#
#Team:Stadium Street Address City State Zip
#
#And uses Google Maps to find the time it takes to drive between each team 
#and each other team. Output is of the format:
#
#Team1:Team2:Time (in x days x hours x mins)
#######################################################

#Make a array of teams and addresses
my @name_address;

my $input_file = 'address_list.txt';

open (INPUT, "<", "$input_file") or die "Cannot open input file: $!";

while(<INPUT>){
    chomp;
    push (@name_address, $_);
}

close (INPUT);

#For each team-team combination, run the get_distance subroutine.
#Print Team1:Team2:Time
foreach my $team (@name_address){
    foreach my $team2 (@name_address){
	if ($team eq $team2){
	    next;
	}
	else{
	    my @stuff = split(':', $team);
	    my @stuff2 = split(':', $team2);
	    my $time = &get_distance($stuff[1], $stuff2[1]);
	    my $toprint = "$stuff[0]".':'."$stuff2[0]".':'."$time";
	    print "$toprint\n";
	}
    }
}

#Takes in 2 addresses, checks google maps, and returns the time
#to drive between the 2 addresses
sub get_distance{
    (my $input1, my $input2) = @_;

#Format the addresses correctly    
    my $start = &make_address($input1);
    my $end = &make_address($input2);

#Get the directions from google maps
    my $url = 'http://maps.googleapis.com/maps/api/directions/json?origin='."$start".'&destination='."$end".'&sensor=false';

#Sleep so that the server will respond correctly
    sleep(1);

    my $json = get($url);

#In the JSON file returned by google maps, the drive time is in the first line that
#says text : after the first line that says duration. Get the time and return it.
    my $switch = 0;

    my @lines = split /\n/, $json;
    foreach my $line (@lines){
	if ($switch == 1){
	    if ($line =~ m/"text" : "([\w\W]+)"/){
		return $1;
		last;
	    }
	}
	elsif ($line =~ m/duration/){
	    $switch = 1;
	}
    }
}

#Replace spaces in the address with +s to put in the google api url.
sub make_address{
    my $address = pop @_;
    $address =~ s/ /\+/g;
    return $address;
}
