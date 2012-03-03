if (badblock) {
	if (omitbad)
		continue;
	memset (readbuf, 0xff, bs);
} else {
	/* Read page data and exit on failure */
	if (pread(fd, readbuf, bs, ofs) != bs) {
		perror("pread");
		goto closeall;
	}   
}   
