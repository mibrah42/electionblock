export const campaigns = [
    {
        title: "US Elections",
        candidates: [
            "Joe Biden",
            "Donald Trump",
            "Bernie Sanders",
            "Abstain from voting",
        ]
    },
    {
        title: "Wakanda Elections",
        candidates: [
            "T'Challa",
            "Erik Killmonger",
            "M'Baku",
            "Abstain from voting",
        ]
    }
];

export const titles = campaigns.map(({title}) => title);