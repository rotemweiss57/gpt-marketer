# from spam_model import SpamClassifier
#
# classifier = SpamClassifier()
#
# # test_email = """Transform Your Marketing Strategy with Streak's Al Capabilities Email to: michaeld@salesforce.com
# # Dear Michael Davis, As the VP of Marketing at Salesforce, you've expertly steered through the complexities of modern
# # marketing, always on the lookout for innovative solutions to elevate your strategies and enhance engagement. In
# # today's era, where personalization isn't just valued but essential, I'm thrilled to present a pioneering tool that
# # aligns seamlessly with Salesforce's vision of delivering outstanding customer experiences-Streak. Streak redefines
# # mass marketing with its cutting-edge Al technology, enabling the creation of highly personalized email campaigns on a
# # large scale. Picture your communications being individually tailored to connect profoundly with each recipient,
# # effectively standing out in overcrowded inboxes and establishing meaningful connections. This is the new era of
# # marketing-where efficiency and personalization converge to not only engage but also drive significant conversions.
# # Your recent initiative, the 'Pro Suite,' aimed at expanding Salesforce's reach within the SMB market, is noteworthy.
# # Streak's Al-driven capabilities could augment these efforts by offering SMBs the ability to effortlessly design
# # personalized marketing campaigns, thereby enhancing the 'Pro Suite's' value. Streak promises to unlock unprecedented
# # levels of customization and efficiency in marketing, aligning perfectly with the 'Pro Suite's' objectives. I am eager
# # to discuss how Streak can integrate with Salesforce's offerings, enabling your SMB clients to revolutionize their
# # marketing strategies and achieve remarkable growth. Let's explore together how we can leverage Al to transform the
# # marketing landscape. Would you be available for a brief call next week to explore this transformative opportunity
# # further? Best regards, Omer Nauer Streak omern@streak.com"""
# #
# # test_email2 = """Elevate Nvidia's Email Strategy with Al-Driven Personalization Email to: treynolds@nvidia.net Dear
# # Terrance Reynolds, In the fast-evolving digital marketing landscape, personalization isn't just an advantage-it's
# # imperative for cutting through the noise and truly connecting with your audience. At Nvidia, your role as a Marketing
# # Strategist places you at the forefront of leveraging technology to craft impactful marketing strategies. We at Streak
# # are thrilled to present a platform that's not just another tool but a transformative solution to elevate your email
# # campaigns. Our Al-driven technology personalizes email communications on a scale previously unimaginable,
# # turning each message into a unique conversation with its recipient. This isn't just personalization; it's
# # personalization with precision and empathy, designed to significantly boost engagement and conversions. The rapid
# # technological advancements, particularly in Al, have reshaped the marketing landscape. Nvidia's contributions to Al
# # and tech innovation have not only pushed boundaries but also demonstrated the immense potential of Al in
# # revolutionizing marketing strategies. It's clear that staying ahead in today's competitive market requires embracing
# # advanced solutions that can deliver truly personalized experiences. Streak's Al platform is a step into the future,
# # enabling Nvidia to send emails that are not just targeted but genuinely resonate with each individual's preferences,
# # interests, and needs. This level of personalization ensures that your communications are impactful and memorable.
# # Let's discuss how Streak can help Nvidia leverage the power of Al for creating email campaigns that set new standards
# # in personalization and engagement. Together, we can redefine what's possible in email marketing and drive
# # unparalleled success for your brand. Thank you for considering Streak as your ally in innovation. We're excited about
# # the prospect of partnering with Nvidia to bring the future of personalized marketing into the present. Warm regards,
# # Omer Nauer Streak omern@streak.com"""
# #
# # test_email3 = """RE: Following Up!
# # Good Morning!
# # Thope you are doing well. I wanted to revisit the previous email I sent last week. I was reaching out to discuss your account and schedule a FREE demo for office supply procurement solutions and savings. To provide you with a comprehensive view of our capabilities, we'd like to offer you a $25 gift card in exchange for your time.
# # Are you available for a brief call next week to delve into these topics and explore how our solutions can benefit your company? Please let me know your availability, and | will ensure a convenient time slot is reserved for you. Or feel free to use the link below to book directly on my calendar!
# # Best,
# # Kerwin Joseph (he/him/his)
# # NYC Territory Manager ^ Staples Business Advantage.
# # BUSINESS IS HUMAN"""
#
# spam_probability = classifier.classify_email(test_email3)
#
# print(f"Probability of being spam: {spam_probability * 100:.2f}%")


import pandas as pd
from spam_model import SpamClassifier

# Load the Excel file
file_path = 'tester_with_results.xlsx'
emails_df = pd.read_excel(file_path)

# Initialize the spam classifier
classifier = SpamClassifier()

# Process each email
for index, row in emails_df.iterrows():
    email_text = row[0]  # Assuming the email text is in the first column
    spam_probability = classifier.classify_email(email_text)
    print(f"Email {index + 1}: Old result: {row[1]*100}%, Probability of being spam: {spam_probability * 100:.2f}%")
