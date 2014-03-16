#!/usr/bin/perl

use warnings;
use strict;

###############################################
#Takes in a list of teams, and a scrubbed html page with a list of MLB team addresses
#of the format:
#
#Team
#Stadium Name
#Street Address
#City, State Zip
#Phone: Phone number
#
#and outputs a file with each team and their stadium address in the format:
#
#Team:Stadium Street Address City, State Zip
###############################################

#Make a list of teams
my @teams;

open (TEAMS, "<", 'team_list.txt') or die "Cannot open team list file: $!";

while(<TEAMS>){
    chomp;
    push (@teams, $_);
}

close (TEAMS);

my $append = 0;
my $address = '';

#Use the scrubbed html page to scrape addresses from
open (WEBPAGE, "<", 'stadium_address_webpage.txt') or die "Cannot open webpage file: $!";

while(<WEBPAGE>){
    chomp;
#The phone number is on the line following the address, so stop appending the address
#when you see the term "Phone"
    if ($_ =~ m/Phone/){
	$append = 0;
	$address =~ s/\s+$//;
	print "$address\n";
    }
#Keep appending the address in the right situation
    elsif ($append == 1){
	$_ =~ s/^\s+//;
	$address = "$address"."$_".' ';
    }
#Print the team name when it's found, and start appending the address from the next line
    foreach my $team (@teams){
	if ($_ =~ m/$team/){
	    $append = 1;
	    $address = "$team".':';
	}
    }
}

close (WEBPAGE);
