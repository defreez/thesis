/**
* msm_nand_oob_64 - oob info for large (2KB) page
*/
static struct nand_ecclayout msm_nand_oob_64 = {
        .eccbytes       = 40,
        .eccpos         = {
                0,  1,  2,  3,  4,  5,  6,  7,  8,  9,
               10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
               20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
               46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
               },
        .oobavail       = 16,
        .oobfree        = {
                {30, 16},

};
