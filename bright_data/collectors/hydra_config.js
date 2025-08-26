module.exports = {
    collectors: [
        {
            name: "price_monitor",
            type: "e_commerce",
            schedule: "*/5 * * * *",
            targets: [
                "competitor1.com",
                "competitor2.com"
            ],
            data_points: [
                "product_name",
                "price",
                "availability",
                "reviews_count",
                "rating"
            ]
        },
        {
            name: "job_spy",
            type: "jobs",
            schedule: "0 */6 * * *",
            platforms: ["linkedin", "indeed"],
            search_queries: [
                "company:competitor1",
                "company:competitor2"
            ],
            extract: [
                "title",
                "department",
                "requirements",
                "salary_range",
                "location"
            ]
        }
    ]
};
