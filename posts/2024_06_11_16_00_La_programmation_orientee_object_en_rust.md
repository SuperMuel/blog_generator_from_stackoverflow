# La programmation orientée objet (POO) en Rust

La programmation orientée objet (POO) est un paradigme de programmation populaire qui permet aux développeurs de structurer leur code en objets contenant des données et des comportements associés. Bien que le langage Rust ne soit pas un langage orienté objet traditionnel comme Java ou C++, il offre une approche différente mais efficace pour atteindre des objectifs similaires grâce à la composition et aux traits.

En Rust, au lieu d'utiliser des classes et l'héritage, vous construisez des objets en combinant des composants réutilisables plus petits à l'aide de structures (structs). Voici un exemple de base pour créer un objet "Voiture" composé de plusieurs parties :

```rust
// Définition d'une structure représentant un moteur
struct Moteur {
    puissance: u32,
}

// Définition d'une structure représentant des roues
struct Roues {
    diametre: f32,
}

// Définition de la structure principale "Voiture"
struct Voiture {
    moteur: Moteur,
    roues: Roues,
    couleur: String,
}

// Création d'une instance de "Voiture"
let ma_voiture = Voiture {
    moteur: Moteur { puissance: 150 },
    roues: Roues { diametre: 16.5 },
    couleur: String::from("Rouge"),
};
```

Dans cet exemple, la `Voiture` est composée d'un `Moteur`, de `Roues` et d'une `couleur`. Vous pouvez ajouter des comportements à vos objets en définissant des méthodes associées à l'aide de blocs `impl`.

La réutilisation du code et le polymorphisme en Rust sont gérés par les traits. Un trait définit un ensemble de méthodes que les types implémentant ce trait doivent fournir. Voici un exemple de trait `Vehicule` qui définit une méthode `demarrer` :

```rust
trait Vehicule {
    fn demarrer(&self) {
        println!("Le véhicule démarre !");
    }
}

// Implémentation du trait Vehicule pour Voiture
impl Vehicule for Voiture {}

fn main() {
    let ma_voiture = Voiture { /* ... */ };
    ma_voiture.demarrer(); // Appelle la méthode demarrer() du trait Vehicule
}
```

Les traits peuvent également être utilisés pour le polymorphisme et le dispatching dynamique grâce aux objets de trait. Cela permet d'écrire du code générique qui fonctionne avec n'importe quel type implémentant un certain trait. Par exemple, considérons le trait `Dessiner` avec une méthode `dessiner` et deux types `Cercle` et `Rectangle` qui l'implémentent :

```rust
trait Dessiner {
    fn dessiner(&self);
}

struct Cercle {
    rayon: f32,
}

impl Dessiner for Cercle {
    fn dessiner(&self) {
        println!("Dessin d'un cercle de rayon {}", self.rayon);
    }
}

struct Rectangle {
    largeur: f32,
    hauteur: f32,
}

impl Dessiner for Rectangle {
    fn dessiner(&self) {
        println!("Dessin d'un rectangle de largeur {} et de hauteur {}", self.largeur, self.hauteur);
    }
}

fn dessiner_forme(forme: &dyn Dessiner) {
    forme.dessiner();
}

fn main() {
    let cercle = Cercle { rayon: 3.0 };
    let rectangle = Rectangle { largeur: 5.0, hauteur: 2.5 };
    dessiner_forme(&cercle);
    dessiner_forme(&rectangle);
}
```

Dans cet exemple, la fonction `dessiner_forme` accepte n'importe quel type qui implémente le trait `Dessiner`. Grâce à cette flexibilité, le code peut fonctionner avec différents types d'objets qui partagent un comportement commun défini par le trait.

En résumé, bien que Rust n'ait pas de support intégré pour les classes et l'héritage traditionnels, il fournit des mécanismes alternatifs efficaces pour atteindre des objectifs similaires. En utilisant judicieusement les structures, les traits et les objets de trait, les développeurs Rust peuvent écrire du code modulaire, composable et maintenable, tout en bénéficiant des avantages de sécurité, de concurrence et de performances offerts par le langage.

### Conclusion

La programmation orientée objet en Rust peut sembler différente de ce que vous connaissez dans les langages orientés objet traditionnels, mais elle offre une approche puissante et flexible. En tirant parti des structures pour créer des objets composés, des traits pour définir des comportements réutilisables et des objets de trait pour le polymorphisme, vous pouvez créer des applications robustes et performantes tout en restant fidèle aux principes de la programmation orientée objet.

### Lectures complémentaires

- [The Rust Programming Language - Chapitre 17: "Object Oriented Programming Features of Rust"](https://doc.rust-lang.org/book/ch17-00-oop.html)
- [Rust Reference Documentation](https://doc.rust-lang.org/reference/)
- [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)
