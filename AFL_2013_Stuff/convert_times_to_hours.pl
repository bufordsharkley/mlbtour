#!/usr/bin/perl

use warnings;
use strict;

open (DISTANCES, "<", 'distances_list.txt') or die "Cannot open input file: $!";

while(<DISTANCES>){
    chomp;
    my @array = split(':', $_);
    my $time = 0;
    if ($array[2] =~ m/(\d+) day/){
	$time = $time + $1 * 24;
    }
    if ($array[2] =~ m/(\d+) hour/){
	$time = $time + $1;
    }
    if ($array[2] =~ m/(\d+) min/){
	$time = $time + $1 / 60;
    }
    my $toprint = join(':', ($array[0], $array[1], $time));
    print "$toprint\n";
}

close (DISTANCES)
