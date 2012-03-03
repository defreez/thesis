def backStep(self, rawData):
  bc = self.minHdrSz
  for f in range(0, len(self.schema)): self.fieldSizes.append(0)
    while bc < self.sliceSz and not self.valid:
      if self.validateHdr(rawData[self.sliceSz-bc:self.sliceSz], bc):
        self.tailingRec = rawData[self.sliceSz-bc:]
        self.valid = True
      bc += 1
