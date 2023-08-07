
function changeEnglishMonthToPersian(className){
    let postDateElements = document.querySelectorAll(`.${className}`)


    let MONTH_ENGLISH_NAMES = ['Farvardin', 'Ordibehesht', 'Khordad', 'Tir', 'Mordad', 'Shahrivar', 'Mehr',
                                'Aban', 'Azar', 'Dey', 'Bahman', 'Esfand'];

    let MONTH_PERSIAN_NAMES = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر',
                          'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'];

    postDateElements.forEach(function(postDate){
        let dateSplit = postDate.innerHTML.split(" ");
        let monthIndex = MONTH_ENGLISH_NAMES.indexOf(dateSplit[2]);
        postDate.innerHTML = `${dateSplit[1]} ${MONTH_PERSIAN_NAMES[monthIndex]} ${dateSplit[0]}`;
    })
}


changeEnglishMonthToPersian("post__date")
changeEnglishMonthToPersian("footer-post__date")


const deleteWrapper = document.getElementById('delete-warning')
const deleteCancelBtn = document.getElementById('delete-cancel')
const postDeletee = document.getElementById('post-delete')


function postDelete(){
    deleteWrapper.classList.add('block');
}

deleteCancelBtn.addEventListener('click', (function(){
    deleteWrapper.classList.remove('block');
}))
