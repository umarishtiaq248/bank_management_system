function change_bank_display(divID){
    document.getElementById("show_banks").style.display = "none";
    document.getElementById("show_account").style.display = "none";
    document.getElementById(divID).style.display = "block";
}
function change_account_display(divID){
    document.getElementById("add_account").style.display = "none";
    document.getElementById("show_accounts").style.display = "none";
    document.getElementById(divID).style.display = "block";
}