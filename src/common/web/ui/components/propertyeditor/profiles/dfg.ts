import { type PropertyProfile } from "../PropertyProfile";

export const dfgDmp: PropertyProfile = {
    metadata: {
        id: ["Deutsche Forschungsgemeinschaft", "21.12.2021"],
        displayLabel: "DFG Profile",
        description: "Deutsche Forschungsgemeinschaft DMP Profile"
    },
    layout: [
        {
            id: "1",
            label: "Datenbeschreibung",
            input: [
                {
                    id: "1",
                    label: "Auf welche Weise entstehen in Ihrem Projekt neue Daten?",
                    type: "textarea",
                    description:
                        "Hier sind Messungen, Befragungen, Fotos, Filme, Analysen, Berechnungen usw. gemeint. Beschreiben Sie möglichst umfassend, welche Methoden Sie benutzen und welche Art von Daten dabei entstehen bzw. welche Sie nutzen werden."
                },
                {
                    id: "2",
                    label: "Werden existierende Daten wiederverwendet?",
                    type: "textarea",
                    description: ""
                },
                {
                    id: "3",
                    label: "Welche Datentypen, im Sinne von Datenformaten (z. B. Bilddaten, Textdaten oder Messdaten) entstehen in Ihrem Projekt und auf welche Weise werden sie weiterverarbeitet?",
                    type: "textarea",
                    description: ""
                },
                {
                    id: "4",
                    label: "In welchem Umfang fallen diese an bzw. welches Datenvolumen ist zu erwarten?",
                    type: "textarea",
                    description: ""
                }
            ],
            required: true
        },
        {
            id: "2",
            label: "Dokumentation und Datenqualität",
            input: [
                {
                    id: "1",
                    label: "Welche Ansätze werden verfolgt, um die Daten nachvollziehbar zu beschreiben (z. B. Nutzung vorhandener Metadaten- bzw. Dokumentationsstandards oder Ontologien)?",
                    type: "textarea",
                    description: ""
                },
                {
                    id: "2",
                    label: "Welche Maßnahmen werden getroffen, um eine hohe Qualität der Daten zu gewährleisten?",
                    type: "textarea",
                    description: ""
                },
                {
                    id: "3",
                    label: "Sind Qualitätskontrollen vorgesehen und wenn ja, auf welche Weise?",
                    type: "textarea",
                    description: ""
                },
                {
                    id: "4",
                    label: "Welche digitalen Methoden und Werkzeuge (z. B. Software) sind zur Nutzung der Daten erforderlich?",
                    type: "textarea",
                    description: ""
                }
            ],
            required: true
        },
        {
            id: "3",
            label: "Speicherung und technische Sicherung während des Projektverlaufs",
            input: [
                {
                    id: "1",
                    label: "Auf welche Weise werden die Daten während der Projektlaufzeit gespeichert und gesichert?",
                    type: "textarea",
                    description: ""
                },
                {
                    id: "2",
                    label: "Wie wird die Sicherheit sensibler Daten während der Projektlaufzeit gewährleistet (Zugriffs- und Nutzungsverwaltung)?",
                    type: "textarea",
                    description: ""
                }
            ],
            required: true
        },
        {
            id: "4",
            label: "Rechtliche Verpflichtungen und Rahmenbedingungen",
            input: [
                {
                    id: "1",
                    label: "Welche rechtlichen Besonderheiten bestehen im Zusammenhang mit dem Umgang mit Forschungsdaten in Ihrem Projekt?",
                    type: "textarea",
                    description: ""
                },
                {
                    id: "2",
                    label: "Sind Auswirkungen oder Einschränkungen in Bezug auf die spätere Veröffentlichung bzw. Zugänglichkeit zu erwarten?",
                    type: "textarea",
                    description: ""
                },
                {
                    id: "3",
                    label: "Auf welche Weise werden nutzungs- und urheberrechtliche Aspekte sowie Eigentumsfragen berücksichtigt?",
                    type: "textarea",
                    description: ""
                },
                {
                    id: "4",
                    label: "Existieren wichtige wissenschaftliche Kodizes bzw. fachliche Normen, die Berücksichtigung finden sollten?",
                    type: "textarea",
                    description: ""
                }
            ],
            required: true
        },
        {
            id: "5",
            label: "Datenaustausch und dauerhafte Zugänglichkeit der Daten",
            input: [
                {
                    id: "1",
                    label: "Welche Daten bieten sich für die Nachnutzung in anderen Kontexten besonders an?",
                    type: "textarea",
                    description: ""
                },
                {
                    id: "2",
                    label: "Nach welchen Kriterien werden Forschungsdaten ausgewählt, um diese für die Nachnutzung durch andere zur Verfügung zu stellen?",
                    type: "textarea",
                    description: ""
                },
                {
                    id: "3",
                    label: "Planen Sie die Archivierung Ihrer Daten in einer geeigneten Infrastruktur? Falls ja, wie und wo?",
                    type: "textarea",
                    description: ""
                },
                {
                    id: "4",
                    label: "Gibt es Sperrfristen? Wann sind die Forschungsdaten für Dritte nutzbar?",
                    type: "textarea",
                    description: ""
                }
            ],
            required: true
        },
        {
            id: "6",
            label: "Verantwortlichkeiten und Ressourcen",
            input: [
                {
                    id: "1",
                    label: "Wer ist verantwortlich für den adäquaten Umgang mit den Forschungsdaten (Beschreibung der Rollen und Verantwortlichkeiten innerhalb des Projekts)?",
                    type: "textarea",
                    description: ""
                },
                {
                    id: "2",
                    label: "Welche Ressourcen (Kosten, Zeit oder anderes) sind erforderlich, um einen adäquaten Umgang mit Forschungsdaten im Projekt umzusetzen?",
                    type: "textarea",
                    description: ""
                },
                {
                    id: "3",
                    label: "Wer ist nach Ende der Laufzeit des Projekts für das Kuratieren der Daten verantwortlich?",
                    type: "textarea",
                    description: ""
                }
            ],
            required: true
        }
    ]
};
