export const campaigns = [
    {
        title: "US Elections",
        candidates: [
            "Donald Trump",
            "Joe Biden",
            "Kanye West",
            "I'll pass this time"
        ]
    },
    {
        title: "Wakanda Elections",
        candidates: [
            "T'Challa",
            "Erik Killmonger",
            "M'Baku"
        ]
    }
];

export const titles = campaigns.map(({title}) => title);