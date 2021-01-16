#!/usr/bin/perl


sub is_valid_update {
    opendir my $dir, "/fw/update";
    my @files = readdir $dir;
    closedir $dir;

    my $archive;
    my $checksum;
    my $version;
    foreach (@files) {
        $file = $_;
        if ( $file =~ /tar.gz/ ) {
            $archive = $file
        } elsif ( $file =~ /md5/ ) {
            $checksum = $file;
        } elsif ( $file =~ /version/ ) {
            $version = `cat $file`;
        }
    }

    if ( defined $archive && defined $checksum and defined $version ) {
        return ( 1, $archive, $checksum, $version )
    } else {
        return ( 0, $archive, $checksum, $version )
    }
}


sub verify_integrity {
    my $archive = @_[0];
    my $checksum = @_[1];
    $archive = "/fw/update/".$archive;
    $checksum "/fw/update/".$checksum;
    $checksum_val = `cat $checksum`;
    $archive_checksum = `md5sum $archive | cut -d ' ' -f 1`;
    $checksum_val = trim $checksum_val;
    $archive_checksum = trim $archive_checksum;
    my $valid_update = 0;
    if ( $archive_checksum == $checksum_val )  {
        $valid_update = 1
    }

    return $valid_update;
}


sub check_for_update {
    if ( -d "/fw/update" ) {
        print "Update available\n";
        my ($valid, $archive, $checksum, $version) = is_valid_update()

        if ( !$valid ) {
            return;
        }

        my $update_not_corrupted = verify_integrity( $archive, $checksum );

        if ( !$update_not_corrupted ) {
            return;
        }

        my $command = "mkdir /fw/app_$version";
        system( $command )
        if ( $? != 0 ) {
            return;
        }

        $command = "tar -xzf /fw/update/$archive -C /fw/app_$version/";
        system( $command )
        if ( $? != 0 ) {
            return;
        }

        my $current_fw_dir = `ls -l /fw/DataLogger | grep app | cut -d '>' - 2`;
        $current_fw_dir = trim $current_fw_dir;
        
        $command = "ln -snf /fw/app_$version /fw/DataLogger/app"
        system( $command )
        if( $? != 0 ) {
            return;
        }

        $command = "rm -rf $current_fw_dir";
        system( $command );

    }
}

check_for_update();

