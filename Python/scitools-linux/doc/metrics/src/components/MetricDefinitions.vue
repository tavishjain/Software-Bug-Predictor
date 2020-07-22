<template>
    <v-row
            align="center"
            class="text--primary"
    >
        <v-col cols="12" v-if="metricDefinitions && lang">
            <v-row align="center">
                <v-col class="d-flex" cols="12" sm="4">
                    <v-select
                            :items="metricDefinitions.metricDropdownOptions[lang]"
                            label="All Metrics"
                            v-model="metricType"
                    ></v-select>
                </v-col>
                <v-col class="d-flex" cols="12" sm="4">
                    <v-select
                            :items="metricDefinitions.languageOptions[lang]"
                            item-text="type"
                            label="All Languages"
                            v-model="languageType"
                    ></v-select>
                </v-col>
                <v-col class="d-flex" cols="12" sm="4">
                    <v-text-field
                            v-model="search"
                            append-icon="search"
                            label="Search"
                            single-line
                    >
                    </v-text-field>
                </v-col>
            </v-row>

            <v-data-table
                    :headers="headers"
                    :items="filteredMetrics"
                    :search="search"
                    :disable-pagination="true"
                    :disable-sort="true"
                    :hide-default-footer="true"
                    :custom-filter="metricSearch"
                    class="elevation-1"
            >
                <template v-slot:body="{ items }">
                    <tbody>
                    <tr v-for="metric in items" :key="metric.name" @click="metricClicked(metric)">
                        <td class="text-no-wrap">{{ metric[lang].metric }}</td>
                        <td class="text-no-wrap">{{ metric[lang].friendly }}</td>
                        <td>{{ metric[lang].systemdesc }}</td>
                    </tr>
                    </tbody>
                </template>
            </v-data-table>
            <language-dialog></language-dialog>
        </v-col>
    </v-row>
</template>

<script>
    import axios from 'axios'
    import {mapMutations, mapState} from "vuex";
    import LanguageDialog from "./LanguageDialog";

    export default {
        name: "MetricDefinitions",
        components: {LanguageDialog},
        data() {
            return {
                search: null,
                dialog: false,
                metricType: 'all',
                languageType: 'all',
                headers: [
                    {text: 'API Name', value: this.lang + '.metric'},
                    {text: 'Friendly Name', value: this.lang + '.friendly'},
                    {text: 'Description', value: this.lang + '.systemdesc'},
                ]
            }
        },
        mounted() {
            document.addEventListener("contextmenu", function(e){
                e.preventDefault();
            }, false);
            let langParam = new URL(window.location.href).searchParams.get('lang');
            if(langParam) {
                let lang = langParam.split('_')[0].toLowerCase() || 'en';
                this.updateLang(lang);
            }
            this.updatePageName('Metric Definitions');

        },
        computed: {
            langgg(){
              return new URL(window.location.href).searchParams.get('lang');
            },
            filteredMetrics() {
                if (!this.metricDefinitions) {
                    return null;
                }
                let filteredMetrics = this.metricDefinitions.metrics;
                if (this.metricType != 'all') {
                    filteredMetrics = filteredMetrics.filter(metric => {
                       return metric[this.lang].hasOwnProperty(this.metricType) && metric[this.lang][this.metricType];
                    });
                }

                if (this.languageType != 'all') {
                    filteredMetrics = filteredMetrics.filter(metric => {
                        return metric[this.lang].hasOwnProperty(this.languageType) && metric[this.lang][this.languageType];
                    });
                }
                return filteredMetrics;

            },
            ...mapState(['metricDefinitions', 'lang'])
        },
        methods: {
            metricSearch (value, search, item) {
                search = search.toLowerCase();
                return !!(item && (item[this.lang].friendly.toLowerCase().includes(search) ||
                    item[this.lang].metric.toLowerCase().includes(search) ||
                    item[this.lang].description.toLowerCase().includes(search)));
            },
            metricClicked(metric) {
                this.updateSelectedMetric(metric);
                this.updateShowDialog(true);
            },
            ...mapMutations(['updatePageName', 'updateMetricDefinitions', 'updateSelectedMetric', 'updateShowDialog', 'updateLang'])
        }
    }
</script>

<style scoped>
    tr:hover td {
        color: #01579B;
        text-decoration: underline;
        cursor: pointer;
    }
</style>