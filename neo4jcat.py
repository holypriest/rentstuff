from py2neo import authenticate, Graph, Node, Relationship

def create_and_relate(categories):
	nodelist = []
	for key in categories:
		leftnode = Node("Categoria", nome=key)
		nodelist.append(leftnode)
		if categories.get(key) is not None:
			rightnodes = create_and_relate(categories.get(key))
			for node in rightnodes:
				rel_product_category = Relationship(leftnode, "TEM_SUBCATEGORIA", node)
				stuffgraph.create(rel_product_category)
	return nodelist

categorias = {
'Antiguidades':
	{
	'Decoração e Cenografia':
		{
		'Móveis': None,
		'Vestuário': None
		},
	'Vestuário':
		{
		'Camisas': None,
		'Calças': None,
		'Sapatos': None
		},
	'Brinquedos':
		{
		'Jogos de tabuleiro': None,
		'Baralhos': None
		},
	'Equipamentos':
		{
		'Máquinas de escrever': None,
		'Câmeras fotográficas': None,
		'Vitrolas e Gramofones': None,
		'Filmadoras': None
		}
	},
'Arte':
	{
	'Pinturas':
		{
		'Originais': None,
		'Reproduções': None
		},
	'Gravuras':
		{
		'Caricaturas': None,
		'Litogravuras': None,
		'Xilogravuras': None
		},
	'Materiais':
		{
		'Telas': None,
		'Pincéis': None,
		'Lápis': None,
		'Canetas': None,
		'Tintas':
			{
			'Acrílicas': None,
			'Óleos': None
			}
		}
	},
'Vestuário':
	{
	'Camisetas': None,
	'Camisas': None,
	'Calças': None,
	'Saias': None,
	'Tênis': None,
	'Sapatos': None
	},
'Eletrônicos':
	{
	'TVs':
		{
		'CRT': None,
		'LCD': None,
		'LED':
			{
			'3D': None
			}
		},
	'Home Theaters': None,
	'Aparelhos de Som': None,
	'Video Games': None
	},
'Esportes':
	{
	'Futebol':
		{
		'Bolas': None,
		'Chuteiras': None,
		'Camisas':
			{
			'Times nacionais': None,
			'Times estrangeiros': None
			}
		},
	'Volei':
		{
		'Bolas': None,
		'Equipamentos de proteção': None
		},
	'Basquete':
		{
		'Bolas': None,
		'Tênis': None
		},
	'Esgrima':
		{
		'Espadas': None,
		'Floretes': None,
		'Sabres': None
		}
	},
'Jogos':
	{
	'Cartas':
		{
		'Baralho': None,
		'Card games': None
		},
	'Tabuleiros':
		{
		'Damas': None,
		'Xadrez':
			{
			'Madeira': None,
			'Pedra': None,
			'Plástico': None
			},
		'Gamão': None,
		'GO': None
		},
	'RPGs':
		{
		'Livros': None,
		'Action Figures': None
		}
	},
'Informática':
	{
	'Computadores':
		{
		'Desktops': None,
		'Notebooks': None
		},
	'Tablets':
		{
		'7 pol.': None,
		'10 pol.': None
		},
	'Smartphones': None
	},
'Filmes':
	{
	'Nacionais':
		{
		'DVDs': None,
		'Blu Ray': None,
		'VHS': None,
		'Betamax': None
		},
	'Estrangeiros':
		{
		'DVDs': None,
		'Blu Ray': None,
		'VHS': None,
		'Betamax': None
		}
	},
'Livros':
	{
	'Nacionais':
		{
		'Ficção': None,
		'Técnicos': None,
		'Biografias': None
		},
	'Estrangeiros':
		{
		'Ficção': None,
		'Técnicos': None,
		'Biografias': None
		}
	},
'Música':
	{
	'Nacionais':
		{
		'CDs': None,
		'Discos de vinil': None,
		'Fitas cassete': None
		},
	'Importados':
		{
		'CDs': None,
		'Discos de vinil': None,
		'Fitas cassete': None
		}
	},
'Brinquedos':
	{
	'Jogos de tabuleiro': None,
	'Action Figures': None,
	'Bonecas': None,
	'Miniaturas':
		{
		'Veículos': None,
		'Construções': None
		}
	}
}

# Popula o banco de dados com nós e relações baseadas no dicionário 'categorias'
authenticate("localhost:7474", "neo4j", "secret")
stuffgraph = Graph()
stuffgraph.delete_all()
create_and_relate(categorias)
