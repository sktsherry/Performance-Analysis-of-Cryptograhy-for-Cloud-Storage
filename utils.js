function download(data, name){
    const a = document.createElement("a"); 
    a.href = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], {
        type: "text/plain"
    }));
    a.setAttribute("download", name);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}