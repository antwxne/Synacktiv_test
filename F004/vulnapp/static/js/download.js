function downloadB64(id_file, filename, container_id){
    fetch('/gallery/download?file=' + filename + '&base64=Y')
    .then(async response => await response.json())
    .then((json_resp) => {
        const img_element = document.createElement('img');
        img_element.src = "data:image/png;base64, " + json_resp.filecontent;
        img_element.id = "downloaded_" + id_file;
        img_element.style.objectFit = 'none' ;
        img_element.style.flex = '0 1' ;
        document.getElementById(container_id).appendChild(img_element);
    })
    .then(() => console.log(id_file + ": downloaded"))
    .catch((error) => console.warn(error));
}
