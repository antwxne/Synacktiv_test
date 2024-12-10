function checkUpload()
{
    const filename = document.getElementById('filetag').value;
    const filesplit = filename.split('.')
    const extension = filesplit[filesplit.length - 1];
    if (extension != 'jpg' && extension != 'png'){
        const fakeFilename = filename.split('\\');
        const trueFilename = fakeFilename[fakeFilename.length - 1];
        var errorMsgTag = document.getElementById('preUploadError');
        errorMsgTag.style.display = 'block';
        errorMsgTag.innerHTML = `'${trueFilename}': wrong file extension (only accept jpg and png)`;
        return false;
    }
}
