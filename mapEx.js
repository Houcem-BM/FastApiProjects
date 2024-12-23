const arr = [
    [1,'houssem', 6],
    [2,'dadi',7],
    [3,'cheraf',8]
]

/*arrObjects = arr.map(([a,b,c])=> ({
    'id':a,
    'name':b,
    'grade':c
}))*/
/*arrObjects = arr.map(item=> ({
    'id':item[0],
    'name':item[1],
    'grade':item[2]
}))*/
arrObjects = arr.map(([id,name,grade])=> ({
    id,
    name,
    grade
}))

console.clear()
console.log(arrObjects)