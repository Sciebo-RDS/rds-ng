<script setup lang="ts">
import Accordion from "primevue/accordion";
import AccordionPanel from "primevue/accordionpanel";
import AccordionHeader from "primevue/accordionheader";
import AccordionContent from "primevue/accordioncontent";
import Panel from "primevue/panel";
import { type PropType, toRefs } from "vue";

import { UserSettings } from "@common/data/entities/user/UserSettings";

import { FrontendComponent } from "@/component/FrontendComponent";
import ExternalLink from "@common/ui/components/misc/ExternalLink.vue";

const comp = FrontendComponent.inject();
const props = defineProps({
    tabData: {
        type: Object as PropType<UserSettings>,
        required: true
    }
});
const propRefs = toRefs(props);
</script>

<template>
    <div class="grid grid-flow-dense grid-cols-1 gap-1.5 w-full h-full">
        <div class="r-text-title">Help &amp; Support</div>
        <Accordion value="0">
            <AccordionPanel value="0">
                <AccordionHeader class="header">About {{ comp.data.title }}</AccordionHeader>
                <AccordionContent class="content" :pt="{ content: 'pl-0' }">
                    <p>
                        {{ comp.data.title }} is designed to facilitate efficient and secure research data management by offering a user-friendly platform that
                        enables researchers to prepare, annotate, and share datasets in line with FAIR principles. This beta portal serves as your central hub
                        for guidance, technical support, and feedback to help us continuously improve the app.
                    </p>
                    <p>
                        Whether you are a researcher managing your data, a developer enhancing the platform, or an administrator overseeing research data
                        sharing infrastructure, you will find tailored resources, detailed tutorials, and answers to frequently asked questions to support your
                        role.
                    </p>
                    <p>
                        Your feedback is crucial in shaping {{ comp.data.title }}’s future. Please feel free to ask questions, report issues, or suggest
                        improvements. Together, we aim to build a robust, transparent, and accessible research data ecosystem that meets the needs of the
                        academic community.
                    </p>
                    <p>
                        What works well? What’s missing? What surprised you? - Please share your feedback directly via
                        <ExternalLink link="mailto:sciebo.rds@uni-muenster.de" text="email" />
                        !
                    </p>
                </AccordionContent>
            </AccordionPanel>

            <AccordionPanel value="1">
                <AccordionHeader class="header">Features</AccordionHeader>
                <AccordionContent class="content" :pt="{ content: 'pl-0' }">
                    <p>
                        {{ comp.data.title }} offers a range of features to support you in sharing your research data efficiently and in compliance with the
                        FAIR data principles:
                    </p>
                    <p>
                        <strong>Connect your data via Sciebo Cloud to repositories such as Zenodo or OSF</strong><br />
                        Easily link your datasets stored in the Sciebo university cloud with established research data repositories to ensure long-term
                        accessibility and visibility.
                    </p>
                    <p>
                        <strong>Manage metadata</strong><br />
                        Maintain and enrich metadata in a structured way and select appropriate licenses to ensure your data can be properly cited, reused, and
                        understood - and the best is: you only have to do it once before and it will be set into your dataset for every upload. This ensures
                        your data safety and defines every further use.
                    </p>
                    <p>
                        <strong>Generate accompanying documentation</strong><br />
                        Automatically create standardized documentation to describe the context, structure, and content of your datasets – helping others (or
                        your future self) to make sense of the data.
                    </p>
                    <p>
                        <strong>Initiate DOI creation</strong><br />
                        Trigger the assignment of a Digital Object Identifier (DOI) for your dataset to ensure persistent referencing and recognition of your
                        research contributions.
                    </p>
                </AccordionContent>
            </AccordionPanel>

            <AccordionPanel value="2">
                <AccordionHeader class="header">Frequently Asked Questions (FAQ)</AccordionHeader>
                <AccordionContent class="content" :pt="{ content: 'pl-0' }">
                    <Panel header="General" :pt="{ root: 'border-none', header: 'pl-0 text-base', content: 'p-0' }">
                        <p>
                            <strong> Who can use {{ comp.data.title }}?</strong><br />
                            {{ comp.data.title }} is available to all registered users of the sciebo cloud, especially researchers at universities in North
                            Rhine-Westphalia (NRW) and their cooperation partners.
                        </p>
                        <p>
                            <strong>Do I need any technical background to use {{ comp.data.title }}?</strong><br />
                            No. {{ comp.data.title }} is designed to be intuitive and user-friendly. No programming knowledge is required.
                        </p>
                        <p>
                            <strong>Is {{ comp.data.title }} free to use?</strong><br />
                            Yes. {{ comp.data.title }} is a free service for users of the sciebo university cloud.
                        </p>
                        <p>
                            <strong>What are the FAIR principles?</strong><br />
                            FAIR stands for Findable, Accessible, Interoperable, and Reusable. These principles ensure that research data can be discovered,
                            accessed, and reused by others in a transparent and meaningful way.
                        </p>
                    </Panel>

                    <Panel header="Uploading & Publishing Data" :pt="{ root: 'border-none mt-4', header: 'pl-0 text-base', content: 'p-0' }">
                        <p>
                            <strong>How do I upload my data from the sciebo cloud?</strong><br />
                            {{ comp.data.title }} connects to your personal sciebo cloud instance. You can select, describe, and annotate the datasets you want
                            to share directly in the app.
                        </p>
                        <p>
                            <strong>Where are my data stored?</strong><br />
                            Your data remain securely stored in your sciebo cloud account. It is only transferred to an external repository (e.g., Zenodo, OSF)
                            when you explicitly choose to upload it.
                        </p>
                        <p>
                            <strong>How do I publish my data to OSF or Zenodo?</strong><br />
                            {{ comp.data.title }} supports direct file uploads and metadata export to repositories like OSF and Zenodo. Once reviewed, the final
                            publication needs to be initiated through the repository's web site.
                        </p>
                    </Panel>

                    <Panel header="Metadata & Documentation" :pt="{ root: 'border-none mt-4', header: 'pl-0 text-base', content: 'p-0' }">
                        <p>
                            <strong>What kind of metadata do I need to provide?</strong><br />
                            You’ll be guided to enter essential metadata such as title, authors, description, keywords, license, and project context. Accurate
                            metadata helps increase the visibility and reusability of your dataset.
                        </p>
                        <p>
                            <strong>Can I add a README or other documentation to my dataset?</strong><br />
                            Yes. {{ comp.data.title }} supports the inclusion of accompanying documentation like README files or data dictionaries. You can
                            upload a README to your sciebo project folder and include it when exporting your dataset to a repository.
                        </p>
                    </Panel>

                    <Panel header="Datasets & Data management" :pt="{ root: 'border-none mt-4', header: 'pl-0 text-base', content: 'p-0' }">
                        <p>
                            <strong>How can I ensure my data complies with my institution’s data management policies?</strong><br />
                            {{ comp.data.title }} does not enforce specific institutional or funder policies but encourages alignment with your institution's
                            best practices. The app supports clear documentation of data sharing processes to help meet common compliance requirements.
                        </p>
                        <p>
                            <strong>Can I restrict access to sensitive data?</strong><br />
                            While {{ comp.data.title }} assists in preparing data for open sharing, you retain full control over what is published. Sensitive or
                            personal data should be anonymized or excluded before publication, as {{ comp.data.title }} cannot take responsibility for verifying
                            anonymity or legal compliance.
                        </p>
                        <p>
                            <strong>Does {{ comp.data.title }} support version control of datasets?</strong><br />
                            Currently, dataset versioning must be managed within the connected repository (e.g., Zenodo).
                        </p>
                    </Panel>

                    <Panel header="Collaboration & Integration" :pt="{ root: 'border-none mt-4', header: 'pl-0 text-base', content: 'p-0' }">
                        <p>
                            <strong>Which data platforms can I connect to {{ comp.data.title }}}?</strong><br />
                            {{ comp.data.title }} currently integrates with Zenodo and OSF (Open Science Framework). Additional platforms may be supported in
                            future releases.
                        </p>
                        <p>
                            <strong>Can I collaborate with other researchers or students?</strong><br />
                            Not yet. {{ comp.data.title }} does not currently support shared workflows via sciebo or repositories. However, it facilitates
                            collaborative dataset preparation by allowing multiple users to work on metadata and documentation jointly before uploading.
                        </p>
                        <p>
                            <strong>Can I reuse previously uploaded datasets in new projects?</strong><br />
                            Yes. If a dataset has been published under a reusable license, it can be cited and reused in future research projects.
                        </p>
                    </Panel>

                    <Panel header="Feedback & Contact" :pt="{ root: 'border-none mt-4', header: 'pl-0 text-base', content: 'p-0' }">
                        <p>
                            <strong>Questions or Feedback</strong><br />
                            We’d love to hear from you! Simply
                            <ExternalLink link="mailto:sciebo.rds@uni-muenster.de" text="send us an email" />
                            to get in touch with us.
                        </p>
                        <p>
                            <strong>Technical Support & Maintenance</strong><br />
                            University of Münster – Center for Information Technology (CIT)
                        </p>
                        <p>
                            <strong>Scientific Coordination</strong><br />
                            University of Potsdam – Chair of Business Information Systems & Digital Transformation
                        </p>
                    </Panel>
                </AccordionContent>
            </AccordionPanel>

            <AccordionPanel value="3">
                <AccordionHeader class="header">Useful links</AccordionHeader>
                <AccordionContent class="content" :pt="{ content: 'pl-0' }">
                    <p>
                        Explore these useful links to deepen your understanding of research data management and to access relevant tools and platforms connected
                        to {{ comp.data.title }}.
                    </p>
                    <div>
                        <ul class="link-list">
                            <li>
                                <strong>{{ comp.data.title }} GitHub Repository</strong><br />
                                Discover the source code, contribute to development, or follow updates on {{ comp.data.title }}’s open-source project.<br />
                                <ExternalLink link="https://github.com/Sciebo-RDS/Sciebo-RDS" text="https://github.com/Sciebo-RDS/Sciebo-RDS" />
                            </li>
                            <li>
                                <strong>Sciebo University Cloud (University of Münster)</strong><br />
                                Access your personal Sciebo cloud storage, the secure environment where your data is stored and managed before publication.<br />
                                <ExternalLink link="https://uni-muenster.sciebo.de" text="https://uni-muenster.sciebo.de" />
                            </li>
                            <li>
                                <strong>Research Data Management Project Page (University of Münster)</strong><br />
                                Learn more about the research data management initiatives at the University of Münster, including current projects, policies,
                                and support services.<br />
                                <ExternalLink
                                    link="https://cris.uni-muenster.de/portal/de/project/54015178"
                                    text="https://cris.uni-muenster.de/portal/de/project/54015178"
                                />
                            </li>
                            <li>
                                <strong>Research Data Management at the University of Potsdam</strong><br />
                                Explore resources, guidelines, and support services for effective research data management provided by the University of
                                Potsdam.<br />
                                <ExternalLink link="https://www.uni-potsdam.de/de/forschungsdaten" text="https://www.uni-potsdam.de/de/forschungsdaten" />
                            </li>
                            <li>
                                <strong>DFG Guidelines on Handling Research Data</strong><br />
                                Understand the standards and best practices recommended by the German Research Foundation (DFG) for responsible research data
                                management.<br />
                                <ExternalLink
                                    link="https://www.dfg.de/foerderung/grundlagen_rahmenbedingungen/forschungsdaten"
                                    text="https://www.dfg.de/foerderung/grundlagen_rahmenbedingungen/forschungsdaten"
                                />
                            </li>
                            <li>
                                <strong>Zenodo Repository</strong><br />
                                A trusted open-access repository where researchers can publish and share datasets, software, and other research outputs with
                                assigned DOIs.<br />
                                <ExternalLink link="https://zenodo.org" text="https://zenodo.org" />
                            </li>
                            <li>
                                <strong>Open Science Framework (OSF)</strong><br />
                                A free, open platform to support researchers in managing, sharing, and collaborating on their research projects and data.<br />
                                <ExternalLink link="https://osf.io" text="https://osf.io" />
                            </li>
                        </ul>
                    </div>
                </AccordionContent>
            </AccordionPanel>
        </Accordion>
    </div>
</template>

<style scoped lang="scss">
.header {
    @apply pl-0;
}

.content {
    @apply text-sm;
}

.content p:not(:last-of-type) {
    @apply mb-4;
}

.link-list li:not(:last-of-type) {
    @apply pb-4;
}
</style>
