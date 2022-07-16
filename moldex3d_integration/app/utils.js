import {FRAPPE_FILE_UPLOAD_ENDPOINT, updateMessage } from "./constant";

export const uploadAttachmentAsFile = (file, doctype, docname, frm) => {
    console.log(`Call extenal : ${doctype}, and name : ${docname}  `)
    let formdata = new FormData();
    formdata.append("is_private", 0);
    //formdata.append("folder", "Home/Attachments"); // "Home/"+frm.doc.doctype
    formdata.append("folder", "Home/"+doctype);
    formdata.append("doctype", doctype);
    formdata.append("docname", docname);
    //imagefile.append('file', file);
    formdata.append("file",file, _filename(docname));    
    //fetch(FRAPPE_FILE_UPLOAD_ENDPOINT, {
    fetch('/api/method/upload_file', {
        headers: {
            /*Accept: "application/json",*/
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
    const title = /*updateMessage*/ "Mac File";
    const total = 100;
    window.frappe.show_progress(title, current,total, description, true);
};
