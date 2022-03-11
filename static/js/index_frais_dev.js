// 'use strict'
const calculer = document.getElementById("calculer")
const repas = document.getElementById("repas")
const nuit = document.getElementById("nuit")
const cotisR = document.getElementById("cotisationsRepas")
const impotR = document.getElementById("impotsRepas")
const cotisN = document.getElementById("cotisationsNuit")
const impotN = document.getElementById("impotsNuit")

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
  const totalForfait = (parseFloat(repas.textContent.replace(',','.')) +
   parseFloat(nuit.textContent.replace(',','.'))).toFixed(2)

   const totalCotisations = (parseFloat(cotisR.textContent.replace(',','.')) +
   parseFloat(cotisN.textContent.replace(',','.'))).toFixed(2)

   const totalImpots = (parseFloat(impotR.textContent.replace(',','.')) +
   parseFloat(impotN.textContent.replace(',','.'))).toFixed(2)

   const resteR = (parseFloat(repas.textContent.replace(',','.')) -
   parseFloat(cotisR.textContent.replace(',','.'))-
   parseFloat(impotR.textContent.replace(',','.'))).toFixed(2)

   const resteN = (parseFloat(nuit.textContent.replace(',','.')) -
   parseFloat(cotisN.textContent.replace(',','.'))-
   parseFloat(impotN.textContent.replace(',','.'))).toFixed(2)

   const resteT = (parseFloat(resteR) + parseFloat(resteN)).toFixed(2)


  // const totalCalcul = parseFloat(repas.innerHTML) + parseFloat(nuit.innerHTML)
  totalRepas[8].innerHTML = totalForfait
  totalRepas[9].innerHTML = totalCotisations
  totalRepas[10].innerHTML = totalImpots
  totalRepas[3].innerHTML = resteR
  totalRepas[7].innerHTML = resteN
  totalRepas[11].innerHTML = resteT

  const tt = document.querySelector('#totalReste')
  tt.style.fontWeight = 'bold'

  const texteR = `Valeur restante pour le repas : <strong>${resteR}€</strong>
   pour la nuit+pdj: <strong>${resteN}€</strong>`
  resultat.innerHTML = texteR
  textResult.append(resultat)

  memocheck()

  return
}

calculer.addEventListener('click', recalcul())
