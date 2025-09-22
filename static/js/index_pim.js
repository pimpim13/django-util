

const form = document.querySelector('.form')
form.addEventListener('change',clearResult)

const formLoad = document.querySelector('.form')
form.addEventListener('DOMContentLoaded',memocheck())






function memocheck(){
  console.log('memecheck')}

function clearResult(){
  console.log('clearResult')
  let b = document.body
  let tableau_sans_tt = document.getElementById('table_sans_tt');

  //let memo_table_1 = b.removeChild(tableau_sans_tt)

  b.remove(tableau_sans_tt)


}
