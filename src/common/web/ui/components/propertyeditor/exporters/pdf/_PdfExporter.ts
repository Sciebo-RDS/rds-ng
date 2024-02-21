// @ts-nocheck

import pdfMake from "pdfmake/build/pdfmake";
import pdfFonts from "pdfmake/build/vfs_fonts";

export class PdfExporterExport {
    static downloadPdf(dD: any, title: string): void {
        (<any>pdfMake).vfs = pdfFonts.pdfMake.vfs;
        const fileName = `DMP_${!!title ? title.replaceAll(" ", "_") : "unnamed"}_${new Date().toLocaleDateString()}.pdf`;
        pdfMake.createPdf(dD).download(fileName);
    }
}
