import {FRAPPE_FILE_UPLOAD_ENDPOINT, updateMessage } from "./constant";

const _filename = (name) => `${name}-MX3d.mac`; //.pdf


export const uploadAttachmentAsFile = (file, doctype, docname, frm) => {
    let formdata = new FormData();
    formdata.append("is_private", 1);
    formdata.append("folder", "Home/Attachments"); // Home/Mac Moldex
    formdata.append("doctype", doctype);
    formdata.append("docname", docname);
    formdata.append("file",file, _filename(docname));
    fetch(FRAPPE_FILE_UPLOAD_ENDPOINT, {
        headers: {
            Accept: "application/json",
            "x-Frappe-CSRF-Token": window.frappe.csrf_token,
        },
        method: "POST",
        body: formdata,
    }).then(()=> {
        showProgress(100, "done");
        //frm.reload_doc();
    });
};
//res => res.json()
export const showProgress = (current, description) => {
    const title = updateMessage;
    const total = 100;
    window.frappe.show_progress(title, current,total, description, true);
};
