const slide =  document.getElementById("formControlRange")
const duree = document.getElementById("duree")

const h_debut = document.querySelector("#h_debut")
const h_fin = document.querySelector("#h_fin")

document.addEventListener('DOMContentLoaded', function() {
  console.log('HTML prêt !');
});


slide.addEventListener('input', () => {
  console.log('change')
  duree.innerHTML = slide.value
})

const form = document.querySelector('.form')
form.addEventListener('change',memocheck)

const memoCheck = document.querySelector('#memoCheck')
memoCheck.addEventListener('change', memocheck)

function setMemo() {
  localStorage.setItem('h_debut',h_debut.value)
  localStorage.setItem('h_fin',h_fin.value)
  localStorage.setItem('slide',slide.value)

  console.log('valeur stockée h_debut :' + h_debut.value, )
  console.log('valeur stockée h_fin :' + h_fin.value, )
  console.log('valeur stockée slide :' + slide.value, )

}

function memocheck(){
  if(memoCheck.checked){
    setMemo()
  }
  else {
    console.log("unchecked")
    localStorage.clear()
  }
}

function setPreferences() {
  h_debut.value = localStorage.getItem('h_debut')
  h_fin.value = localStorage.getItem('h_fin')
  slide.value = localStorage.getItem('slide')
  duree.innerHTML = slide.value

  console.log('valeur lue h_debut :' + h_debut.value, )
  console.log('valeur lue h_fin :' + h_fin.value, )
  console.log('valeur lue slide :' + slide.value, )
}

if(localStorage.getItem('h_debut')){
  console.log(localStorage.getItem('h_debut'))
  setPreferences()

}
else {
  memocheck()
}






// application des preferences
