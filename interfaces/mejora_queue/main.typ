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
  #text([Mejora de diseño], weight: 900, size: 18pt)
// ]

= Problemas

- No se lista el tiempo de espera
- No se pueden hacer acciones en el momento de espera
- No se tiene confirmación sobre el asiento

= Preguntas 

- ¿Por qué hay una cola? ¿Para permitir la elección exclusiva de una persona a la vez?
- ¿Podemos eliminar la cola?

= Solución

En caso de que no sea posible eliminar la cola.

+ Preselección:
  - El usuario entra en un modo de preselección de asientos
  - Hay instrucciones claras y concisas que le indican que seleccione en orden de prioridad los asientos que le gustaría tener. También hay un enlace para una descripción más larga y clara.
  - Hay _signifiers_ y _constraints_ sobre asientos que ya fueron seleccionados definitivamente, los cuales indican visualmente que no están disponibles y no permite realizar acciones sobre ellos.
  - Hay _signifiers_ sobre los asientos más probables a ser seleccionados por usuarios en cola. Se conoce esto porque todos pasan por la fase de preselección
  - El usuario elige, con orden de prioridad, distintos asientos que quiere. Marca su primera opción, segunda por si le ganan el primero, tercera opción, etc.
  - Los asientos preseleccionados indican su número de prioridad directamente, por ejemplo con un número.
  
+ Espera
  - Una vez seleccionados los asientos, se le dice al usuario que le llegará una notificación Push y un correo sobre el estatus de los asientos seleccionados.
  - Siempre puede volver a la aplicación y editar los asientos antes de que sea su turno.
  - Cada vez que un asiento deseado se ocupa, se informa al usuario con notificaciones.
  - Cuando todos los asientos se llenen, se informa al usuario.

+ Turno
  - Si el usuario no vuelve a entrar a la aplicación se selecciona su asiento en su turno basado en la preselección.
  - Si el usuario entra antes de su turno puede hacer cambios sobre los asientos elegidos.
