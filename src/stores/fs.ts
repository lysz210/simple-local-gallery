export const useFsStore = defineStore('fs', {
  state: () => ({
    previewSelecetedPhotos: false,
    selectedPhotos: {} as Record<string, string[]>,
  }),
  actions: {
    removeSelectedPhoto(folder: string, photo: string) {
      if (!this.selectedPhotos[folder]) {
        return;
      }
      this.selectedPhotos[folder] = this.selectedPhotos[folder].filter(p => p !== photo)
    }
  }
})