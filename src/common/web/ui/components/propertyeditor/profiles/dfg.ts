import { type PropertyProfile, PropertyDataType } from "../PropertyProfile";

export const dfgDmp: PropertyProfile = {
    profile_id: { name: "Deutsche Forschungsgemeinschaft", version: "21.12.2021" },
    categories: [
        {
            id: "1",
            name: "Datenbeschreibung",
            properties: [
                {
                    id: "1",
                    name: "Auf welche Weise entstehen in Ihrem Projekt neue Daten?",
                    type: PropertyDataType.TEXTAREA,
                    description:
                        "Hier sind Messungen, Befragungen, Fotos, Filme, Analysen, Berechnungen usw. gemeint. Beschreiben Sie möglichst umfassend, welche Methoden Sie benutzen und welche Art von Daten dabei entstehen bzw. welche Sie nutzen werden.",
                    showAlways: true,
                },
                {
                    id: "2",
                    name: "Werden existierende Daten wiederverwendet?",
                    type: PropertyDataType.TEXTAREA,
                    description: "",
                    showAlways: true,
                },
                {
                    id: "3",
                    name: "Welche Datentypen, im Sinne von Datenformaten (z. B. Bilddaten, Textdaten oder Messdaten) entstehen in Ihrem Projekt und auf welche Weise werden sie weiterverarbeitet?",
                    type: PropertyDataType.TEXTAREA,
                    description: "",
                    showAlways: true,
                },
                {
                    id: "4",
                    name: "In welchem Umfang fallen diese an bzw. welches Datenvolumen ist zu erwarten?",
                    type: PropertyDataType.TEXTAREA,
                    description: "",
                    showAlways: true,
                },
            ],
        },
        {
            id: "2",
            name: "Dokumentation und Datenqualität",
            properties: [
                {
                    id: "1",
                    name: "Welche Ansätze werden verfolgt, um die Daten nachvollziehbar zu beschreiben (z. B. Nutzung vorhandener Metadaten- bzw. Dokumentationsstandards oder Ontologien)?",
                    type: PropertyDataType.TEXTAREA,
                    description: "",
                    showAlways: true,
                },
                {
                    id: "2",
                    name: "Welche Maßnahmen werden getroffen, um eine hohe Qualität der Daten zu gewährleisten?",
                    type: PropertyDataType.TEXTAREA,
                    description: "",
                    showAlways: true,
                },
                {
                    id: "3",
                    name: "Sind Qualitätskontrollen vorgesehen und wenn ja, auf welche Weise?",
                    type: PropertyDataType.TEXTAREA,
                    description: "",
                    showAlways: true,
                },
                {
                    id: "4",
                    name: "Welche digitalen Methoden und Werkzeuge (z. B. Software) sind zur Nutzung der Daten erforderlich?",
                    type: PropertyDataType.TEXTAREA,
                    description: "",
                    showAlways: true,
                },
            ],
        },
        {
            id: "3",
            name: "Speicherung und technische Sicherung während des Projektverlaufs",
            properties: [
                {
                    id: "1",
                    name: "Auf welche Weise werden die Daten während der Projektlaufzeit gespeichert und gesichert?",
                    type: PropertyDataType.TEXTAREA,
                    description: "",
                    showAlways: true,
                },
                {
                    id: "2",
                    name: "Wie wird die Sicherheit sensibler Daten während der Projektlaufzeit gewährleistet (Zugriffs- und Nutzungsverwaltung)?",
                    type: PropertyDataType.TEXTAREA,
                    description: "",
                    showAlways: true,
                },
            ],
        },
        {
            id: "4",
            name: "Rechtliche Verpflichtungen und Rahmenbedingungen",
            properties: [
                {
                    id: "1",
                    name: "Welche rechtlichen Besonderheiten bestehen im Zusammenhang mit dem Umgang mit Forschungsdaten in Ihrem Projekt?",
                    type: PropertyDataType.TEXTAREA,
                    description: "",
                    showAlways: true,
                },
                {
                    id: "2",
                    name: "Sind Auswirkungen oder Einschränkungen in Bezug auf die spätere Veröffentlichung bzw. Zugänglichkeit zu erwarten?",
                    type: PropertyDataType.TEXTAREA,
                    description: "",
                    showAlways: true,
                },
                {
                    id: "3",
                    name: "Auf welche Weise werden nutzungs- und urheberrechtliche Aspekte sowie Eigentumsfragen berücksichtigt?",
                    type: PropertyDataType.TEXTAREA,
                    description: "",
                    showAlways: true,
                },
                {
                    id: "4",
                    name: "Existieren wichtige wissenschaftliche Kodizes bzw. fachliche Normen, die Berücksichtigung finden sollten?",
                    type: PropertyDataType.TEXTAREA,
                    description: "",
                    showAlways: true,
                },
            ],
        },
        {
            id: "5",
            name: "Datenaustausch und dauerhafte Zugänglichkeit der Daten",
            properties: [
                {
                    id: "1",
                    name: "Welche Daten bieten sich für die Nachnutzung in anderen Kontexten besonders an?",
                    type: PropertyDataType.TEXTAREA,
                    description: "",
                    showAlways: true,
                },
                {
                    id: "2",
                    name: "Nach welchen Kriterien werden Forschungsdaten ausgewählt, um diese für die Nachnutzung durch andere zur Verfügung zu stellen?",
                    type: PropertyDataType.TEXTAREA,
                    description: "",
                    showAlways: true,
                },
                {
                    id: "3",
                    name: "Planen Sie die Archivierung Ihrer Daten in einer geeigneten Infrastruktur? Falls ja, wie und wo?",
                    type: PropertyDataType.TEXTAREA,
                    description: "",
                    showAlways: true,
                },
                {
                    id: "4",
                    name: "Gibt es Sperrfristen? Wann sind die Forschungsdaten für Dritte nutzbar?",
                    type: PropertyDataType.TEXTAREA,
                    description: "",
                    showAlways: true,
                },
            ],
        },
        {
            id: "6",
            name: "Verantwortlichkeiten und Ressourcen",
            properties: [
                {
                    id: "1",
                    name: "Wer ist verantwortlich für den adäquaten Umgang mit den Forschungsdaten (Beschreibung der Rollen und Verantwortlichkeiten innerhalb des Projekts)?",
                    type: PropertyDataType.TEXTAREA,
                    description: "",
                    showAlways: true,
                },
                {
                    id: "2",
                    name: "Welche Ressourcen (Kosten, Zeit oder anderes) sind erforderlich, um einen adäquaten Umgang mit Forschungsdaten im Projekt umzusetzen?",
                    type: PropertyDataType.TEXTAREA,
                    description: "",
                    showAlways: true,
                },
                {
                    id: "3",
                    name: "Wer ist nach Ende der Laufzeit des Projekts für das Kuratieren der Daten verantwortlich?",
                    type: PropertyDataType.TEXTAREA,
                    description: "",
                    showAlways: true,
                },
            ],
        },
    ],
};
