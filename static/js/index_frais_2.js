// 'use strict'
const calculer = document.getElementById("calculer")
const repas = document.getElementById("repas")
const nuit = document.getElementById("nuit")
const cotisR = document.getElementById("cotisationsRepas")
const impotR = document.getElementById("impotsRepas")
const cotisN = document.getElementById("cotisationsNuit")
const impotN = document.getElementById("impotsNuit")

// const plusR = document.querySelector('#plusR')
// const moinsR = document.querySelector('#moinsR')
// const plusN = document.querySelector('#plusN')
// const moinsN = document.querySelector('#moinsN')

// const nbR = document.querySelector('#nbR')
// const nbN = document.querySelector('#nbN')

const repasRef =  parseFloat(repas.textContent.replace(',','.'))
const nuitRef = parseFloat(nuit.textContent.replace(',','.'))
const cotisRRef = parseFloat(cotisR.textContent.replace(',','.'))
const impotRef = parseFloat(impotR.textContent.replace(',','.'))
const cotisNRef = parseFloat(cotisationsNuit.textContent.replace(',','.'))
const impotNRef = parseFloat(impotN.textContent.replace(',','.'))



// let nombreRepas = 1
let nombreRepas = 1
let nombreNuit = 1

// plusR.addEventListener('click',() => {
//   nbR.value = parseInt(nbR.value) + 1
//   nombreRepas = parseInt(nbR.value)
//   recalcul()
// })

// moinsR.addEventListener('click',() => {
//   if(nbR.value >= 1)
//     nbR.value = parseInt(nbR.value) - 1
//     nombreRepas = parseInt(nbR.value)
//     recalcul()
// })

// plusN.addEventListener('click',() => {
//   nbN.value = parseInt(nbN.value) + 1
//   nombreNuit = parseInt(nbN.value)
//   recalcul()
// })

// moinsN.addEventListener('click',() => {
//   if(nbN.value >= 1)
//     nbN.value = parseInt(nbN.value) - 1
//     nombreNuit = parseInt(nbN.value)
//     recalcul()
// })

// nbR.addEventListener('keydown', e => {
//     if(e.key === 'Enter'){
//       nombreRepas = parseInt(nbR.value)
//       console.log(e.key, nombreRepas)
//       recalcul()
//       }
//   })
//
// nbN.addEventListener('keydown', e => {
//     if(e.key === 'Enter'){
//       nombreNuit = parseInt(nbN.value)
//       console.log(e.key, nombreNuit)
//       recalcul()
//       }
//   })


const textResult = document.getElementById("textResult")
const resultat = document.createElement('p')

const totalRepas = document.getElementsByTagName("td")
const totalReste = document.getElementById('totalReste')

const taux = document.getElementById('id_taux')
const localisation = document.getElementById('id_localisation')
const college = document.getElementById('id_college')

const memo = document.getElementById('id_memo')
memo.addEventListener('change', memocheck)

const form = document.querySelector('.form')
form.addEventListener('change',memocheck)


if(localStorage.getItem('taux')){
  setPreferences()

}
else {
  memocheck()
}


// application des preferences
function setPreferences() {
  taux.options[localStorage.getItem('taux')].selected = true
  localisation.options[localStorage.getItem('localisation')].selected = true
  college.options[localStorage.getItem('college')].selected = true
}


// Enregistrement local des preferences
function setMemo() {
  localStorage.setItem('taux',taux.options.selectedIndex)
  localStorage.setItem('localisation',localisation.options.selectedIndex)
  localStorage.setItem('college',college.options.selectedIndex)

}


// verification de la cochr se souvenir de moi et maj des données ou suppression du stockage local
function memocheck(){

  if(memo.checked){
    setMemo()
  }
  else {
    console.log("unchecked")
    localStorage.clear()
  }
}


  // calcul des totaux horizontaux et verticaux du tableau
function recalcul(){

   const totalForfait = (repasRef + nuitRef).toFixed(2)
   const totalRepasForfait = (repasRef * nombreRepas).toFixed(2)
   const totalNuitForfait = (nuitRef * nombreNuit).toFixed(2)


   const xCR = (cotisRRef * nombreRepas).toFixed(2)
   const xIR = (impotRef * nombreRepas).toFixed(2)

   let yCN = (cotisNRef * nombreNuit).toFixed(2)
   let yIN = (impotNRef * nombreNuit).toFixed(2)

   let totalGeneralForfait = (parseFloat(totalRepasForfait) + parseFloat(totalNuitForfait)).toFixed(2)
   let totalCotisations = (parseFloat(xCR) + parseFloat(yCN)).toFixed(2)
   let totalImpots  = (parseFloat(xIR) + parseFloat(yIN)).toFixed(2)


   // const totalCotisations = (cotisRRef + cotisNRef).toFixed(2)
   // const totalImpots = (impotRef + impotNRef).toFixed(2)

   const resteR = (totalRepasForfait - xCR - xIR).toFixed(2)
   const resteN = (totalNuitForfait - yCN - yIN).toFixed(2)

   const resteT = (parseFloat(resteR) + parseFloat(resteN)).toFixed(2)

  totalRepas[8].innerHTML = totalForfait
  // totalRepas[14].innerHTML = totalGeneralForfait

  totalRepas[9].innerHTML = totalCotisations
  totalRepas[10].innerHTML = totalImpots
  totalRepas[3].innerHTML = resteR
  totalRepas[7].innerHTML = resteN
  totalRepas[11].innerHTML = resteT

  // totalRepas[2].innerHTML = totalRepasForfait
  // totalRepas[3].innerHTML = xCR
  // totalRepas[4].innerHTML = xIR
  //
  // totalRepas[8].innerHTML = totalNuitForfait
  // totalRepas[9].innerHTML = yCN
  // totalRepas[10].innerHTML = yIN


  const tt = document.querySelector('#totalReste')
  tt.style.fontWeight = 'bold'

  const texteR = `Valeur restante pour le repas : <strong>${resteR}€</strong>
   pour la nuit+pdj: <strong>${resteN}€</strong> soit un total de
    <strong>${resteT}€<strong>`
  resultat.innerHTML = texteR
  textResult.append(resultat)

  memocheck()

  return
}

calculer.addEventListener('click', recalcul())
