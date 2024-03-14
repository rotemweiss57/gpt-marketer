from spam_model import SpamClassifier

classifier = SpamClassifier()

test_email = """Transform Your Marketing Strategy with Streak's Al Capabilities Email to: michaeld@salesforce.com 
Dear Michael Davis, As the VP of Marketing at Salesforce, you've expertly steered through the complexities of modern 
marketing, always on the lookout for innovative solutions to elevate your strategies and enhance engagement. In 
today's era, where personalization isn't just valued but essential, I'm thrilled to present a pioneering tool that 
aligns seamlessly with Salesforce's vision of delivering outstanding customer experiences-Streak. Streak redefines 
mass marketing with its cutting-edge Al technology, enabling the creation of highly personalized email campaigns on a 
large scale. Picture your communications being individually tailored to connect profoundly with each recipient, 
effectively standing out in overcrowded inboxes and establishing meaningful connections. This is the new era of 
marketing-where efficiency and personalization converge to not only engage but also drive significant conversions. 
Your recent initiative, the 'Pro Suite,' aimed at expanding Salesforce's reach within the SMB market, is noteworthy. 
Streak's Al-driven capabilities could augment these efforts by offering SMBs the ability to effortlessly design 
personalized marketing campaigns, thereby enhancing the 'Pro Suite's' value. Streak promises to unlock unprecedented 
levels of customization and efficiency in marketing, aligning perfectly with the 'Pro Suite's' objectives. I am eager 
to discuss how Streak can integrate with Salesforce's offerings, enabling your SMB clients to revolutionize their 
marketing strategies and achieve remarkable growth. Let's explore together how we can leverage Al to transform the 
marketing landscape. Would you be available for a brief call next week to explore this transformative opportunity 
further? Best regards, Omer Nauer Streak omern@streak.com"""

spam_probability = classifier.classify_email(test_email)

print(f"Probability of being spam: {spam_probability * 100:.2f}%")
