document.addEventListener('DOMContentLoaded', function () {
    let barChart = null;
    let pieChart = null;

    document.getElementById('urlForm').addEventListener('submit', async function (event) {
        event.preventDefault();

        const youtubeUrl = document.getElementById('youtubeUrl').value;
        const loadingDiv = document.getElementById('loading');
        const resultsDiv = document.getElementById('results');

        loadingDiv.style.display = 'block';
        resultsDiv.style.display = 'none';

        try {
            // Fetch comments and process them
            const sentimentResponse = await fetch('http://127.0.0.1:8000/analyze_comments/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: youtubeUrl })
            });

            if (!sentimentResponse.ok) {
                throw new Error('Failed to analyze sentiment.');
            }

            const { videoDetails, sentimentData } = await sentimentResponse.json();
            console.log('Sentiment Response:', videoDetails, sentimentData);

            // Display the results
            loadingDiv.style.display = 'none';
            resultsDiv.style.display = 'block';

            document.getElementById('VideoTitle').innerHTML = `<strong> Video Title: </strong>${videoDetails[2]}`;
            document.getElementById('ChannelName').innerHTML = `<strong> Channel Name: </strong>${videoDetails[1]}`;
            // document.getElementById('ChannelId').innerHTML = `<strong> Channel ID: </strong>${videoDetails[0]}`;

            const avgPolarity = document.getElementById('avgPolarity');
            const mostposcomment = document.getElementById('mostposcomment');
            const mostnegcomment = document.getElementById('mostnegcomment');

            avgPolarity.innerHTML = `<strong> Average Polarity: </strong> ${sentimentData.average_polarity.toFixed(4)}`;
            mostposcomment.innerHTML = `<strong> Most Positive Comment: </strong> ${sentimentData.most_positive_comment}`;
            mostnegcomment.innerHTML = `<strong> Predicted Negative Comment: </strong> ${sentimentData.most_negative_comment}`;


            // Destroy existing charts if they exist
            if (barChart) {
                barChart.destroy();
            }
            if (pieChart) {
                pieChart.destroy();
            }

            // Create charts
            barChart = new Chart(document.getElementById('barChart').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: ['Positive', 'Negative', 'Neutral'],
                    datasets: [{
                        label: 'Number of Comments',
                        data: [
                            sentimentData.positive_count,
                            sentimentData.negative_count,
                            sentimentData.neutral_count
                        ],
                        backgroundColor: ['#28a745', '#dc3545', '#ffc107']
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });

            pieChart = new Chart(document.getElementById('pieChart').getContext('2d'), {
                type: 'pie',
                data: {
                    labels: ['Positive', 'Negative', 'Neutral'],
                    datasets: [{
                        label: 'Sentiment Distribution',
                        data: [
                            sentimentData.positive_count,
                            sentimentData.negative_count,
                            sentimentData.neutral_count
                        ],
                        backgroundColor: ['#28a745', '#dc3545', '#ffc107']
                    }]
                },
                options: {
                    responsive: true
                }
            });

        } catch (error) {
            loadingDiv.style.display = 'none';
            resultsDiv.style.display = 'none';
            console.error('Error:', error);
            alert(`Error: ${error.message}`);
        }
    });

    document.getElementById('CommentForm').addEventListener('submit', async function (event) {
        event.preventDefault();

        const comment = document.getElementById('comment').value;
        const loadingDiv = document.getElementById('loading');
        const resultsDiv = document.getElementById('toxicresults');

        // Show loading indicator and hide results
        loadingDiv.style.display = 'block';
        resultsDiv.style.display = 'none';

        try {
            // Send the comment for sentiment and toxicity analysis
            const CommentResponse = await fetch('http://127.0.0.1:8000/comment_analyze/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ comments: [comment] })
            });

            if (!CommentResponse.ok) {
                throw new Error('Failed to analyze sentiment.');
            }

            const CommentData = await CommentResponse.json();
            console.log('Comment Response:', CommentData);

            // Hide loading and display the results
            loadingDiv.style.display = 'none';
            resultsDiv.style.display = 'block';

            // Fill in the toxicity analysis results
            const BoolToxicityData = CommentData.resultBool[0];
            const INTtoxicityData = CommentData.resultINT[0];

            // Format the results for display
            const formatResult = (boolValue, intValue) => {
                const formattedIntValue = intValue.toFixed(2); // Format to 2 decimal places
                return `${boolValue ? 'Yes' : 'No'}   :   ${formattedIntValue}`;
            };

            // Fill in the toxicity analysis results from the INT results
            document.getElementById('commentText').innerHTML = `<strong> Comment: </strong>${INTtoxicityData.comment_text}`;
            document.getElementById('toxic').innerText = formatResult(BoolToxicityData.is_toxic, INTtoxicityData.toxic);
            document.getElementById('severeToxic').innerText = formatResult(BoolToxicityData.is_severe_toxic, INTtoxicityData.severe_toxic);
            document.getElementById('obscene').innerText = formatResult(BoolToxicityData.is_obscene, INTtoxicityData.obscene);
            document.getElementById('threat').innerText = formatResult(BoolToxicityData.is_threat, INTtoxicityData.threat);
            document.getElementById('insult').innerText = formatResult(BoolToxicityData.is_insult, INTtoxicityData.insult);
            document.getElementById('identityHate').innerText = formatResult(BoolToxicityData.is_identity_hate, INTtoxicityData.identity_hate);

        } catch (error) {
            // Hide loading and display error
            loadingDiv.style.display = 'none';
            resultsDiv.style.display = 'none';
            console.error('Error:', error);
            alert(`Error: ${error.message}`);
        }
    });
});