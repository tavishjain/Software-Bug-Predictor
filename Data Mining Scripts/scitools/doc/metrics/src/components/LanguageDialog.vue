<template>
    <v-dialog
            v-if="selectedMetric"
            v-model="dialog"
    >
        <v-card>
            <v-card-title
                    class="headline primary white--text"
                    primary-title
            >
                {{ selectedMetric[lang].friendly }}
            </v-card-title>
            <v-card-text class="mt-2">
                <div>
                    <strong>API Name:</strong> {{ selectedMetric[lang].metric }}
                </div>
                <div v-if="selectedMetric[lang].research">
                    <strong>Research Name:</strong> {{ selectedMetric[lang].research }}
                </div>
                <div class="text--primary">
                    {{ selectedMetric[lang].description }}
                </div>
            </v-card-text>


            <v-card color="grey lighten-2" class="mx-2 my-4 elevation-2" v-if=" ! selectedMetric.noImage">
                <v-img
                       class="elevation-1"
                       :max-height="height"
                       contain
                       :src="imgSrc"
                >
                </v-img>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on }">
                        <v-btn
                                absolute
                                dark
                                fab
                                top
                                right
                                color="#ff0000"
                                v-on="on"
                                @click="toggleEnlargeImage"
                        >

                            <v-icon v-if="height == baseHeight">mdi-plus</v-icon>
                            <v-icon v-else>mdi-minus</v-icon>
                        </v-btn>
                    </template>
                    <span v-if="height == baseHeight">Enlarge Image</span>
                    <span v-else>Shrink Image</span>
                </v-tooltip>

            </v-card>

            <v-card class="mx-2 my-4 elevation-2">
                <v-list>
                    <v-subheader>Available For</v-subheader>
                    <v-list-item v-for="language in availableLanguages" :key="language.metric"
                                 class="ml-4 text--primary py-0">
                        <v-list-item-content class="py-0">
                            <v-list-item-title>{{ language.type }}</v-list-item-title>
                            <v-list-item-subtitle>{{ selectedMetric[lang][language.value].replace(/,/g, ', ') }}
                            </v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
            </v-card>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                        text
                        @click="updateShowDialog(false)"
                >
                    Close
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
    import {mapMutations, mapState} from "vuex";

    export default {
        name: "LanguageDialog",
        data() {
            return {
                height: '400px',
                baseHeight: '400px',
                enlargedHeight: '900px',
            }
        },
        computed: {
            availableLanguages() {
                return this.metricDefinitions.languageOptions[this.lang].filter(language => {
                    let key = language.value;
                    return this.selectedMetric[this.lang].hasOwnProperty(key) && this.selectedMetric[this.lang][key];
                });
            },
            imgSrc() {
                return 'media/' + this.selectedMetric[this.lang].metric + 'C.png'
            },
            dialog: {
                // getter
                get: function () {
                    return this.showDialog;
                },
                // setter
                set: function (shouldShow) {
                    this.updateShowDialog(shouldShow);
                }
            },
            ...mapState(['metricDefinitions', 'selectedMetric', 'showDialog', 'lang'])
        },
        methods: {
            toggleEnlargeImage() {
                if (this.height == this.baseHeight) {
                    this.height = this.enlargedHeight;
                } else {
                    this.height = this.baseHeight;
                }
            },
            ...mapMutations(['updateShowDialog'])
        }
    }
</script>

<style scoped>
    .v-list-item__content {
        padding: 0;
    }
</style>