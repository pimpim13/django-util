"use strict"
// stockage local des préférences Frais
class FraisStorage{

  constructor(name){
    this.name = name
    this.list = this.get()
  }

  get(){
    if (!localStorage.getItem(this.name)) {
      localStorage.setItem(this.name, '[]')
      console.log('pas de de fichier de memo trouvé')
    }

    const dede = JSON.parse(localStorage.getItem(this.name))
    console.log('dede : ' + dede)
    return dede
    // return [2, 19, 1]
    // return[]
  }

  set(value){
    console.log('valeur stockée : ' + value)
    this.list.push(value)
    this.list.shift()

    if (!localStorage.setItem(this.name, JSON.stringify(this.list)))
      console.log('stockage raté')
    }

  clear(){
    localStorage.removeItem(this.name)

}
}
