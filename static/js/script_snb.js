const slideSnb =  document.getElementById("formControlRange")
const snb_val = document.getElementById("snb_val")

const slideInflation = document.getElementById("formControlRangeInflation")
const inflation_val = document.getElementById("inflation_val")

inflation_val.innerHTML = slideInflation.value
snb_val.innerHTML = slideSnb.value

const nr = document.querySelector('#id_Nr')
const ech = document.querySelector('#id_echelon')
const majres = document.querySelector('#id_maj_res')
const tpstrv = document.querySelector('#id_tps_trav')
const nrFutur = document.querySelector('#id_Nr_futur')
const echFutur = document.querySelector('#id_echelon_futur')


slideSnb.addEventListener('input', () => {
  snb_val.innerHTML = slideSnb.value
})

slideInflation.addEventListener('input', () => {
  inflation_val.innerHTML = slideInflation.value
})

nr.addEventListener('change', ()=> {
  if(nr.value > nrFutur.value){
    nrFutur.options.selectedIndex = nr.options.selectedIndex
    }
})

ech.addEventListener('change', ()=> {
  if(nr.value > echFutur.value){
    echFutur.options.selectedIndex = ech.options.selectedIndex
    }
})

const form = document.querySelector('.form')
form.addEventListener('change',memocheck)

const memoCheck = document.querySelector('#id_memo')

memoCheck.addEventListener('change', memocheck)

function memocheck(){  if(memoCheck.checked){
    setMemo()

  }
  else {
    localStorage.clear()
  }
}

function setMemo(){
    localStorage.setItem('nr',nr.options.selectedIndex)
    localStorage.setItem('echelon',ech.options.selectedIndex)
    localStorage.setItem('maj_res',majres.options.selectedIndex)
    localStorage.setItem('tps_trav',tpstrv.options.selectedIndex)
    localStorage.setItem('nr_futur',nrFutur.options.selectedIndex)
    localStorage.setItem('ech_futur',echFutur.options.selectedIndex)
    localStorage.setItem('inflation',slideInflation.value)
    localStorage.setItem('snb',slideSnb.value)

}


function setPreferences(){
    nr.options[localStorage.getItem('nr')].selected = true
    ech.options[localStorage.getItem('echelon')].selected = true
    majres.options[localStorage.getItem('maj_res')].selected = true
    tpstrv.options[localStorage.getItem('tps_trav')].selected = true
    nrFutur.options[localStorage.getItem('nr_futur')].selected = true
    echFutur.options[localStorage.getItem('ech_futur')].selected = true
    slideSnb.value = localStorage.getItem('snb')
    slideInflation.value = localStorage.getItem('inflation')
    snb_val.innerHTML = slideSnb.value
    inflation_val.innerHTML = slideInflation.value

}

if(localStorage.getItem('nr')){
  //console.log(localStorage.getItem('nr'))
  setPreferences()

}
else {
  memocheck()
}
