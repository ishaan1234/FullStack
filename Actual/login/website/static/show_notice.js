function shownotice(moreId, btnId) {
    var moreText = document.getElementById(moreId);
    var btnText = document.getElementById(btnId);

    if (moreText.style.display === "none" || moreText.style.display === "") {
        moreText.style.display = "inline";
        btnText.innerHTML = "Read Less";
    } else {
        moreText.style.display = "none";
        btnText.innerHTML = "Read More";
    }
}

