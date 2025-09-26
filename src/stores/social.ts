import type { FlickrState } from "@/slg-api"
import { Flickr } from "@/slg-api/sdk.gen"

export const useSocialStore = defineStore('social', {
    state: () => ({
        flickrUser: null as FlickrState | null
    }),
    getters: {
        isFlickrActive: (state) => !!state.flickrUser
    },
    actions: {
        async login() {
            if (!this.flickrUser) {
                const { data: response } = await Flickr.login()
                if (response?.redirect_uri) {
                    window.open(response.redirect_uri)
                } else {
                    this.flickrUser = response?.state ?? null
                }
            }
        }
    }
})