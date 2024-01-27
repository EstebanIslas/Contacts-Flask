const btn_delete = document.querySelectorAll('.btn_delete')

if (btn_delete) {
    const btnArray = Array.from(btn_delete);
    btnArray.forEach((btn)=>{
        btn.addEventListener('click', (e)=>{
            if (!confirm('Are you sure yo want to delete it?')) {
                e.preventDefault();
            }
        });
    });
}