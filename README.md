# SLOAN MIT Conference Submission Work
## The Growth Chart Technique for Analyzing Baseball Counting Statistics
### Erich Rentz and Michael Petersen


**The submitted abstract:**

Baseball hitters’ counting stats grow over the course of a season in much the same way that infants grow over the course of their first year of life. While an infant’s development results in growth spurts and lulls that vary the growth of their weight, height, and head circumference, hitters go through streaks and slumps that vary the growth of their Runs, RBIs, and HRs. Pediatricians and parents use growth charts as means for monitoring this longitudinal progression. In this same way, we have applied the growth chart concept as a means of simplifying, tracking, analyzing, forecasting, and displaying the development of hitters over the course of a season. 

This paper presents the growth chart technique for analyzing baseball hitters. The paper posits that the growth chart technique is an elegant and simple solution for understanding longitudinal baseball datasets by revealing emergent behavior at the mesoscale. The technique is accomplished for a given counting statistic (Runs, RBI, HR, etc.) in three phases: 1) an individual player’s statistic is plotted longitudinally against percentile curves for all hitters at their position; 2) a linear regression is fitted for that player’s counting statistic; 3) a series of linear regressions are fitted to every three week period across the dataset and plotted to show growth rate changed. The visualizations provide context, while the linear regressions reduce dimensionality and promote player comparison. For example, a k-means clustering algorithm run on the linear regressions produced for the universe of players’ Runs production to produce 2017 hitter archetype clusters. The method characterizes players that are having sustained success, like Whit Merrifield, from those who have experienced cold and hot streaks over the season, like Domingo Santana and Mallex Smith respectively.

The growth chart technique is both a way to model hitters and a tool for simplifying, tracking, analyzing, forecasting, and displaying a hitter’s trends. Instead of focusing on aggregate season totals or disaggregate game results, this analysis presents a mesoscale resolution which aligns with and highlights longitudinal hitting trends. The goal of this digestible format is to enable more attention on analysis of a series of players at any level of baseball for any counting statistic. Moreover, the technique also allows comparison across players and epochs. We are currently using the growth chart technique to find and contextualize players who are establishing positive hitting trends from players who are experiencing inconsistent production and believe it could benefit personnel decision-makers at many levels of baseball. Lastly, many baseball statistics are opaque to the casual baseball fan, and this technique can and should be accessible to a wider audience in helping understand how players perform compared to other players at their position. 

**Notebooks**


| Name                   | Contents                          |
|------------------------|-----------------------------------|
|Growth-Chart-Constructor| Build Growth Charts and save      |


