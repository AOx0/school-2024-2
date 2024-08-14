#import "@preview/hidden-bib:0.1.1": *

#set text(size: 13pt, lang: "es")
#set par(justify: true)

#grid(
  columns: (1fr,) * 2,
  inset: 0pt,
  align(left)[
    Interfaces Hombre-Máquina\
    Daniel Alejandro Osornio López\
  ],
  align(right)[
    Universidad Panamericana\
    0244685\@up.edu.mx
  ]
)

#v(1cm)

// #align(center)[
  #text([¿Qué hace un buen diseño?], weight: 900, size: 18pt)
// ]

Un buen diseño es capaz de crear conceptos universales para que las personas puedan interactuar con el servicio de forma que resulta natural y que es imposible usar mal. Hace que el producto que hay detrás de él sea llamativo, visualmente atractivo, pero más importante, que sea útil y comprensible.

Para lograrlo no es necesario crear elementos complejos, sino que son los pequeños detalles los que resultan en una suma que hace sentido y se siente bien. No tiene por qué ser complejo, uno de los retos más grandes es lograr proveer los elementos justos para la interacción, sin sobre poblar el espacio del usuario.

Porque un buen diseño logra el justo medio, sin ser más complejo de lo necesario, es fundamental tomar en cuenta el producto y las necesidades que busca llenar para proveer un diseño que logra el equilibrio entre funcionalidad, extensibilidad, flexibilidad, usabilidad, confiabilidad. 

Ejemplo, no tiene el mismo diseño de lenguaje Rust que Python, cada uno busca resolver ciertos tipos de necesidades y diseñan sobre estos, a nadie le gustaría un Python donde para hacer un script básico hay que declarar tiempos de vida de objetos en memoria. Estas diferencias afectan el nivel de complejidad y la forma en como se presenta al usuario.

Idealmente, un diseño no depende de modas, no debe parecer viejo ni sentirse antiguo o desactualizado. El buen diseño es universal, dura en el tiempo.

Un buen diseño tampoco depende de las capacidades de las personas, si se puede incluir al universo de personas por medio de interacciones naturales, que hacen sentido, no hay necesidad de requerir que la persona cuente con conocimiento específico sobre el producto y lo que hace.



#hidden-citations[
  @tesseract
  @agne_vei
]

#bibliography("bib.yml", title: "Referencias")

