function CategorySelector({ onSelect }) {

    const categories = [
        {
            name: "Network",
            description: "Internet, Wi-Fi and connectivity problems",
        },
        {
            name: "System Performance",
            description: "CPU, memory and storage related problems",
        },
        {
            name: "Authentication",
            description: "Login, password and account problems",
        },
    ];


    return (
        <div className="category-container">

            <h2>Select a problem category</h2>

            <div className="category-grid">

                {categories.map((category) => (

                    <button
                        key={category.name}
                        className="category-card"
                        onClick={() => onSelect(category.name)}
                    >

                        <h3>{category.name}</h3>

                        <p>{category.description}</p>

                    </button>

                ))}

            </div>

        </div>
    );
}


export default CategorySelector;