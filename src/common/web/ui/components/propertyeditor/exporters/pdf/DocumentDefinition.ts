import type { ProfileID, PropertyCategory } from "../../PropertyProfile";
import { PropertyController } from "@common/ui/components/propertyeditor/PropertyController";

interface DocumentDefinition {
    controller: PropertyController<any>;
    profileId: ProfileID;
    pageSize: string;
    header: [{ [string: string]: string }];
    content: [];
    styles: {
        title: {
            fontSize: number;
            bold: boolean;
            margin: number[];
        };
        header: {
            fontSize: number;
            bold: boolean;
            margin: number[];
        };
        subheader: {
            fontSize: number;
            bold: boolean;
            margin: number[];
        };
        footer: {
            margin: number[];
            color: string;
        };
        logo: {
            alignment: string;
        };
    };
    images: { [string: string]: string };
    footer: {
        columns: { text: string; alignment: string };
    };

    buildDocumentDefinition(): any;
}

export class DmpDocumentDefinition implements DocumentDefinition {
    controller;
    profileId;
    pageSize;
    header;
    content;
    styles;
    images;
    footer;

    constructor(controller: PropertyController<any>, profileId: ProfileID) {
        this.controller = controller;
        this.profileId = profileId;
        this.pageSize = "A4";
        this.header = [];
        this.header.push({
            style: "title",
            layout: "noBorders",
            table: {
                widths: ["*", "*"],
                body: [["Data Management Plan"]],
            },
        });
        this.content = [];
        this.styles = {
            title: {
                fontSize: 17,
                bold: true,
                margin: [0, 20, 0, 20],
            },
            header: {
                fontSize: 15,
                bold: true,
                margin: [0, 20, 0, 10],
            },
            subheader: {
                fontSize: 14,
                bold: true,
                margin: [0, 20, 0, 10],
            },
            footer: {
                margin: [20, 20, 20, 20],
                color: "#aaaaaa",
            },
            logo: {
                alignment: "right",
            },
        };
        this.footer = {
            columns: [
                {
                    text: `${profileId.name}, version ${profileId.version["raw"]}.`,
                    alignment: "right",
                },
            ],
            style: "footer",
        };
        this.images = { logo: "" };
    }

    public set logoImage(image: string) {
        this.images["logo"] = image;
        const logoDefinition = {
            image: "logo",
            fit: [100, 100],
            style: "logo",
        };

        this.header[0].table.body[0].push(logoDefinition);
    }

    public set title(title: string) {
        this.header[0].table.body[0][0] = title;
    }

    public addCurrentDate() {
        this.header.push({
            text: `Date: ${new Date().toLocaleDateString()}`,
        });
    }

    public addToc(heading: string = "Content") {
        this.content.push({
            toc: {
                id: "toc",
                title: { text: heading, style: "header" },
            },
        });
    }

    public addCategory(category: PropertyCategory) {
        const categoryHeader = this._makeCategoryHeader(category.name);
        const categoryProperties = this._makeCategoryProperties(category.id, category.properties);

        this.content.push(categoryHeader);

        this.content.push(categoryProperties);
    }

    private _makeCategoryHeader(categoryName: string): {} {
        return {
            style: "header",

            pageBreak: "before",
            layout: "noBorders",
            table: {
                widths: ["*"],
                body: [[{ text: categoryName, fillColor: "green", tocItem: ["toc"], margin: [5, 5, 5, 5] }]],
            },
        };
    }

    private _makeCategoryProperties(categoryId: string, properties): {} {
        let categoryProperties = [];
        for (const property of properties) {
            const propertyData = this.controller.getValue(this.profileId, categoryId, property.id);
            categoryProperties.push({ text: property.name, style: "subheader" });
            const answer = propertyData ? propertyData : "No answer";
            categoryProperties.push(answer);
        }
        return categoryProperties;
    }

    public set footerText(text: string) {
        this.footer.columns[0].text = text;
    }

    public buildDocumentDefinition(): {} {
        let documentDefinition = {
            pageSize: this.pageSize,
            content: [...this.header, ...this.content],
            styles: this.styles,
            images: this.images,
            footer: this.footer,
        };

        return documentDefinition;
    }
}
