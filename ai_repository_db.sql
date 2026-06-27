-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 26, 2026 at 07:44 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ai_repository_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `category_id` int(11) NOT NULL,
  `category_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`category_id`, `category_name`) VALUES
(4, 'AI'),
(2, 'Career'),
(3, 'Education'),
(5, 'Embedded Systems'),
(1, 'Programming');

-- --------------------------------------------------------

--
-- Table structure for table `favorites`
--

CREATE TABLE `favorites` (
  `favorite_id` int(11) NOT NULL,
  `prompt_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `favorites`
--

INSERT INTO `favorites` (`favorite_id`, `prompt_id`, `user_id`) VALUES
(2, 3, 5);

-- --------------------------------------------------------

--
-- Table structure for table `models`
--

CREATE TABLE `models` (
  `model_id` varchar(100) NOT NULL,
  `model_name` varchar(100) NOT NULL,
  `provider` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `models`
--

INSERT INTO `models` (`model_id`, `model_name`, `provider`) VALUES
('anthropic/claude-sonnet-4.6', 'Claude Sonnet', 'Anthropic'),
('google/gemini-2.5-flash', 'Gemini Flash', 'Google'),
('openai/gpt-4o-mini', 'GPT-4o Mini', 'OpenAI');

-- --------------------------------------------------------

--
-- Table structure for table `projects`
--

CREATE TABLE `projects` (
  `project_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `title` varchar(150) NOT NULL,
  `description` text NOT NULL,
  `status` varchar(50) DEFAULT 'Idea'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `projects`
--

INSERT INTO `projects` (`project_id`, `category_id`, `user_id`, `title`, `description`, `status`) VALUES
(2, 2, 5, 'test 1', 'test 1', 'Idea');

-- --------------------------------------------------------

--
-- Table structure for table `project_prompts`
--

CREATE TABLE `project_prompts` (
  `project_prompt_id` int(11) NOT NULL,
  `project_id` int(11) NOT NULL,
  `prompt_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `project_prompts`
--

INSERT INTO `project_prompts` (`project_prompt_id`, `project_id`, `prompt_id`) VALUES
(1, 2, 2),
(2, 2, 3),
(3, 2, 4);

-- --------------------------------------------------------

--
-- Table structure for table `prompts`
--

CREATE TABLE `prompts` (
  `prompt_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `title` varchar(150) NOT NULL,
  `prompt_text` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `prompts`
--

INSERT INTO `prompts` (`prompt_id`, `category_id`, `user_id`, `title`, `prompt_text`, `created_at`) VALUES
(2, 3, 5, 'test prompt 2', 'test prompt 2', '2026-06-25 11:28:40'),
(3, 4, 5, 'test prompt', 'test prompt', '2026-06-25 12:28:55'),
(4, 3, 5, 'capital of pakistan sice day 1', 'what is the capital of pakistan sice day 1 and how and why it changed ?', '2026-06-25 12:45:20');

-- --------------------------------------------------------

--
-- Table structure for table `prompt_executions`
--

CREATE TABLE `prompt_executions` (
  `execution_id` int(11) NOT NULL,
  `prompt_id` int(11) NOT NULL,
  `model_id` varchar(100) NOT NULL,
  `user_id` int(11) NOT NULL,
  `response_text` text NOT NULL,
  `execution_time` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `prompt_executions`
--

INSERT INTO `prompt_executions` (`execution_id`, `prompt_id`, `model_id`, `user_id`, `response_text`, `execution_time`) VALUES
(1, 4, 'openai/gpt-4o-mini', 5, 'The capital of Pakistan has changed since the country was established in 1947. Initially, the capital was Karachi, which served as the capital from 1947 until 1963. Karachi was chosen because it was the largest city and a major commercial hub, as well as being located near the coast, which facilitated trade.\n\nHowever, in 1963, the capital was moved to Islamabad. The decision to shift the capital was part of a broader plan to have a more centrally located and purpose-built capital city. Islamabad was chosen for several reasons:\n\n1. **Geographical location**: Islamabad is situated in the northern part of the country, which makes it more central compared to Karachi. This was seen as important for administrative efficiency and national unity.\n\n2. **Planned city**: Unlike Karachi, which had developed organically over time, Islamabad was designed as a planned city by the Greek architect Constantinos A. Doxiadis. The design incorporated modern urban planning principles, green spaces, and infrastructure intended to accommodate the needs of a growing government and population.\n\n3. **Security**: Post-independence, security concerns were growing, and a location like Islamabad, situated away from the coast and within the more mountainous terrain, was perceived to be less vulnerable to external threats.\n\n4. **Economic and political balance**: Moving the capital to Islamabad was also seen as a way to foster development in the northern regions of Pakistan and reduce the dominance of Karachi and Sindh province in national politics and economy.\n\nTherefore, while Karachi played a significant role as the initial capital, the strategic, political, and practical considerations led to the establishment of Islamabad as the capital of Pakistan in 1963, a status it retains to this day.', '2026-06-25 12:45:52'),
(2, 4, 'google/gemini-2.5-flash', 5, 'The capital of Pakistan has not been the', '2026-06-25 14:53:34'),
(3, 4, 'google/gemini-2.5-flash', 5, 'The capital of Pakistan has not been the same since day one. Here\'s how and why it changed:\n\n**From Day 1 (1947): Karachi**\n\nWhen Pakistan gained independence on August 14, 1947, **Karachi** was declared its first capital.\n\n*   **Why Karachi?**\n    *   **Largest City and Economic Hub:** Karachi was already the largest city in the newly formed nation and a major port, making it a natural choice for an administrative center and economic powerhouse.\n    *   **Infrastructure:** It had existing infrastructure from the British Raj that could support a new government.\n    *   **Proximity to the Sea:** Its coastal location facilitated trade and communication with the outside world.\n\n**Change to Islamabad (1960s):**\n\nThe capital was officially moved from Karachi to **Islamabad** in the early 1960s, though the construction and full transition took several years.\n\n*   **Why the', '2026-06-25 14:53:49'),
(4, 4, 'openai/gpt-4o-mini', 5, 'The capital of Pakistan has changed once since the country gained independence in 1947. \n\n1. **Karachi (1947-1963)**: When Pakistan was formed in 1947, Karachi was chosen as the capital. At that time, Karachi was the largest city and a major commercial hub, making it a logical choice for the capital.\n\n2. **Islamabad (1963-Present)**: In the early 1960s, the government decided to move the capital from Karachi to Islamabad. The reasons for this shift included:\n\n   - **Geographic and Strategic Location**: Islamabad was chosen for its more central location in relation to the country\'s northern borders and as a way to promote development in a less populated area.\n   - **Planned City**: Unlike Karachi, which was a sprawling city, Islamabad was designed as a planned city. This allowed for better urban planning, infrastructure, and administration.\n   - **Security Concerns**: Karachi is located near the coast and was considered vulnerable to attacks and natural disasters. The location of Islamabad, further inland, was seen as more secure.\n\nThus, Islamabad has served as the capital of Pakistan since 1963, reflecting the country\'s administrative and strategic needs.', '2026-06-25 14:55:32'),
(5, 4, 'anthropic/claude-sonnet-4.6', 5, '# Capital of Pakistan: History of Change\n\n## ????️ Day 1 Capital — **Karachi**\n\nWhen Pakistan gained independence on **August 14, 1947**, **Karachi** was chosen as the **first capital**.\n\n### Why Karachi was chosen:\n- It was the **largest and most developed city**\n- Had a **major seaport** (important for trade)\n- Better **infrastructure** compared to other cities\n- Had existing **government buildings** and facilities\n- Was the commercial and economic hub\n\n---\n\n## ???? Why and How the Capital Changed\n\n### Problems with Karachi:\n- **Overpopulation** and rapid urban growth\n- Too far from the **geographic center** of Pakistan\n- **Security concerns** — coastal city, vulnerable to attack\n- **Political and ethnic tensions** in the city\n- Difficult to manage government from a commercial hub\n\n---\n\n## ????️ New Capital — **Islamabad**\n\n### Decision:\n- In **1958**, the government decided to build a **brand new capital city**\n- Greek planner and architect **Constantinos Doxiadis** designed the city\n- Location chosen near **Rawalpindi** in northern Pakistan\n\n### Why Islamabad was chosen:\n- More **centrally located** (closer to center of country)\n- **Strategic** — away from borders and coast\n- **Cooler climate**\n- Near **Rawalpindi** (major military headquarters)\n- Fresh start — no existing urban problems\n- Symbol of **modern, planned Pakistan**\n\n### Timeline:\n| Year | Event |\n|------|-------|\n| 1947 | Karachi becomes first capital |\n| 1958 | Decision made to build new capital |\n| 1966 | Government officially moved to **Islamabad** |\n| 1969 | Islamabad formally declared the capital |\n\n---\n\n## ???? Summary\n\n| | Karachi | Islamabad |\n|--|---------|-----------|\n| **Capital period** | 1947–1966 | 1966–present |\n| **Location** | South (coastal) | North (inland) |\n| **Type** | Existing city | Planned city |\n| **Reason** | Ready infrastructure | Strategic & central |\n\nIslamabad remains the **capital of Pakistan to this day**.', '2026-06-25 16:46:03'),
(6, 4, 'google/gemini-2.5-flash', 5, 'The capital of Pakistan since its inception in 1947 was **Karachi**.\n\nHere\'s how and why it changed:\n\n**From Karachi to Islamabad:**\n\n*   **Initial Capital (1947 - 1959): Karachi**\n    *   **Why Karachi was chosen:** As the largest city, a major port, and a relatively developed urban center in the new country, Karachi made logical sense as the initial capital. It had the infrastructure and existing administrative buildings to quickly set up the government.\n\n*   **Temporary Capital (1959 - 1967): Rawalpindi**\n    *   **Why the move to Rawalpindi:** In 1959, the capital was temporarily shifted from Karachi to Rawalpindi. This was primarily due to the decision to build a new, purpose-built capital city. Rawalpindi, being close to the chosen site for the new capital, served as a convenient interim administrative center while construction was underway.\n\n*   **Permanent Capital (1967 - Present): Islamabad**\n    *   **Why Islamabad was created and chosen:** The decision to build a new capital, Islamabad, was a deliberate and strategic one, driven by several key factors:\n        1.  **Geographical & Strategic Location:** Karachi, being on the coast, was considered vulnerable to sea attacks. Islamabad, located in the Potohar Plateau near the Margalla Hills, offered a more central, secure, and geographically diverse location within the country. It was also closer to the disputed territory of Kashmir, which was a significant political consideration.\n        2.  **Climate:** Karachi\'s hot and humid climate was seen as less conducive to productivity compared to the more temperate climate of the northern regions.\n        3.  **Decongestion and New Identity:** Karachi was becoming increasingly congested, and the government desired a new capital that would embody the aspirations of the young nation, free from the existing urban sprawl and political pressures of a large commercial center. It was intended to be a symbol of Pakistan\'s modern identity.\n        4.  **Equal Distribution of Development:** Establishing a capital in the northern part of the country was also seen as a way to promote development and economic activity in other regions, rather than concentrating everything in the south.\n        5.  **Ayub Khan\'s Vision:** The decision was largely spearheaded by President Ayub Khan, who envisioned a modern, planned capital city. The master plan for Islamabad was developed by Greek architect Constantinos Doxiadis.\n\nThe construction of Islamabad began in the early 1960s, and it was formally declared the capital in **1967**, taking over from Rawalpindi. Since then, Islamabad has remained the capital of Pakistan.', '2026-06-25 17:02:57'),
(7, 2, 'openai/gpt-4o-mini', 5, 'It looks like you\'re testing a prompt. How can I assist you further? If you have a specific question or topic in mind, feel free to share!', '2026-06-25 18:43:50'),
(8, 3, 'openai/gpt-4o-mini', 5, 'It looks like you\'re testing a prompt! How can I assist you today? If you have any specific questions or topics in mind, feel free to share!', '2026-06-25 18:43:53'),
(9, 4, 'openai/gpt-4o-mini', 5, 'The capital of Pakistan has changed since the country\'s independence in 1947. Here’s a brief overview:\n\n1. **Karachi (1947-1963)**: Upon gaining independence in 1947, Karachi was designated as the capital of Pakistan. It was the largest city and a major hub for trade and commerce, which made it a practical choice for the capital during the early years of the country.\n\n2. **Islamabad (1963-Present)**: In 1963, the capital was moved from Karachi to Islamabad. The decision was made by President Ayub Khan, who aimed to create a new capital that would serve as a center of administration that was less vulnerable to the political and economic issues that Karachi faced, such as congestion, overpopulation, and security concerns. Islamabad was selected because it was strategically located in the northern part of the country, near military and political boundaries, and also offered a more planned urban environment.\n\nThe move to Islamabad allowed for more organized urban planning and provided a neutral ground for Pakistan\'s different ethnic groups. The city was built specifically to serve as the capital, with modern architecture and infrastructure designed to accommodate government functions.\n\nSo, as of now, Islamabad has been the capital of Pakistan since 1963, and it is expected to remain the capital for the foreseeable future.', '2026-06-25 18:43:58'),
(10, 2, 'openai/gpt-4o-mini', 5, 'It seems like you\'re testing the prompt functionality. How can I assist you further? If you have a specific question or topic in mind, feel free to share!', '2026-06-25 18:46:11'),
(11, 3, 'openai/gpt-4o-mini', 5, 'It looks like you\'re testing the prompt feature! How can I assist you today? If you have any questions or topics you\'d like to discuss, feel free to share!', '2026-06-25 18:46:13'),
(12, 4, 'openai/gpt-4o-mini', 5, 'The capital of Pakistan has changed since the country gained independence in 1947. Here’s a brief overview of the situation:\n\n1. **Karachi (1947-1963)**: Upon gaining independence from British rule in 1947, Karachi was designated as the capital of Pakistan. At the time, Karachi was the largest city in the country and had significant infrastructure, trade, and cultural importance. However, as the country grew, various issues such as overpopulation, congestion, and inadequate infrastructure became evident.\n\n2. **Islamabad (1963-Present)**: In 1963, the capital was moved from Karachi to Islamabad. This decision was made during President Ayub Khan\'s government. The reasons for this change included:\n\n   - **Geographical Location**: Islamabad\'s location in the northern part of Pakistan was seen as more strategically central to the country. This location was also more accessible to the northern regions, which were becoming increasingly important.\n   \n   - **Planned City**: Islamabad was designed as a modern and planned city, with the intention of creating a functional administrative and governmental hub. The city was planned by the Greek architect Constantinos Doxiadis and incorporated modern urban design principles, which included green spaces and better infrastructure.\n\n   - **Political Stability**: The move was also intended to provide more stability in governance, as Karachi had become increasingly tumultuous and complex politically and socially.\n\nSince then, Islamabad has remained the capital of Pakistan and is noted for its modern architecture and well-planned layout compared to many other cities in the country.', '2026-06-25 18:46:18'),
(13, 2, 'openai/gpt-4o-mini', 5, 'It seems you mentioned \"test prompt 2.\" How may I assist you with it? If you have a specific question or topic in mind, feel free to share!', '2026-06-26 05:00:12'),
(14, 3, 'openai/gpt-4o-mini', 5, 'It looks like you\'re testing the prompt! How can I assist you today? If you have any specific questions or topics you\'d like to discuss, feel free to share!', '2026-06-26 05:00:14'),
(15, 4, 'openai/gpt-4o-mini', 5, 'The capital of Pakistan since its creation in 1947 has been Islamabad. However, the history of Pakistan\'s capital city is a bit more complex due to its temporary governance after independence.\n\nInitially, after Pakistan gained independence from British India in August 1947, Karachi was chosen as the capital. Karachi remained the capital during the formative years of the nation. However, several challenges prompted the government to consider relocating the capital. \n\nBy the 1950s, Karachi faced numerous issues, including overpopulation, inadequate infrastructure, and vulnerability to natural disasters. Additionally, its geographical location in the southern part of the country posed logistical concerns regarding governance and development in the northern and western areas.\n\nTo address these challenges, the government decided to construct a new capital. Islamabad was chosen as it was located in a more central position in the country, had a healthier climate, and was considered to be more strategically secure. The plan for the new city was laid out in the 1960s by the Greek architect Constantinos Apostolou Doxiadis. \n\nIslamabad officially became the capital of Pakistan in 1963. Since then, it has remained the capital and is known for its modern architecture, greenery, and as a center for political and diplomatic activities in Pakistan.', '2026-06-26 05:00:20'),
(17, 2, 'google/gemini-2.5-flash', 5, 'I need a bit more to go on! \"Test prompt 2\" is very general.\n\nTo help me give you a good response, please tell me:\n\n*   **What kind of test is this?** (e.g., a test of my knowledge, a test of my creative writing, a test of my ability to follow instructions, a technical test)\n*   **What should I be testing for or demonstrating?** (e.g., my ability to summarize, my understanding of a concept, my problem-solving skills, my creativity)\n*   **Is there a specific topic or area you want me to address?** (e.g., provide information about AI, write a story about a cat, solve a math problem)\n*   **Are there any constraints or specific instructions I need to follow?** (e.g., keep it under 100 words, use a specific tone, answer in a particular format)\n\n**For example, you could say:**\n\n*   \"Test prompt 2: Write a 3-sentence summary of the plot of \'The Lord of the Rings\'.\"\n*   \"Test prompt 2: Explain the concept of photosynthesis in simple terms.\"\n*   \"Test prompt 2: Generate a list of five unique business ideas for a small town.\"\n*   \"Test prompt 2: Respond to this prompt with a haiku about nature.\"\n\nOnce you give me more details, I can give you a helpful and relevant response!', '2026-06-26 05:02:25'),
(18, 3, 'google/gemini-2.5-flash', 5, 'This is an open-ended prompt! To give you the best and most helpful response, I need a little more information.\n\nPlease tell me:\n\n* **What kind of \"test prompt\" are you looking for?**\n    * **Creative writing?** (e.g., \"Write a short story about...\")\n    * **Technical writing?** (e.g., \"Explain how X works...\")\n    * **Problem-solving?** (e.g., \"Design a solution for Y...\")\n    * **Analytical?** (e.g., \"Compare and contrast A and B...\")\n    * **Code related?** (e.g., \"Write a Python function to...\")\n    * **General knowledge?** (e.g., \"What is the capital of...\")\n    * **Something else entirely?**\n\n* **What is the purpose of this test prompt?**\n    * **To gauge my capabilities?**\n    * **To practice your own writing/thinking?**\n    * **To generate ideas for a project?**\n    * **To have some fun?**\n\n* **Is there a specific topic or theme you\'d like the prompt to be about?**\n\nOnce I have a better understanding of your needs, I can provide a much more specific and useful \"test prompt.\"\n\n**In the meantime, here are a few general examples of test prompts, just to get us started:**\n\n**Example 1 (Creative Writing):**\n> \"You open an old, unmarked box and find an object that shouldn\'t exist. Describe the object, your immediate reaction, and what you decide to do with it.\"\n\n**Example 2 (Analytical/Problem-Solving):**\n> \"Imagine you are tasked with designing a new public park for a bustling urban area. What are three key considerations you would prioritize, and how would you incorporate them into your design to maximize both usability and aesthetic appeal?\"\n\n**Example 3 (Technical/Explanatory):**\n> \"Explain the core concept of \'machine learning\' to someone who has no technical background, using an analogy that makes it easy to understand.\"\n\nLooking forward to hearing more about what you\'re looking for!', '2026-06-26 05:02:30'),
(19, 4, 'google/gemini-2.5-flash', 5, 'The capital of Pakistan has not been the same since day one. Here\'s how and why it changed:\n\n**Capital at Independence (Day 1): Karachi**\n\nWhen Pakistan gained independence on **August 14, 1947**, **Karachi** was declared its first capital.\n\n**Why Karachi was initially chosen:**\n\n*   **Major Port City:** Karachi was already a well-established and thriving port city, crucial for trade and international connections.\n*   **Economic Hub:** It was a significant economic and industrial center, with existing infrastructure and commercial networks.\n*   **Existing Infrastructure:** As a former British Indian provincial capital (of Sindh), it had a relatively developed administrative infrastructure, including government buildings, communication networks, and housing.\n*   **Accessibility:** Its coastal location made it accessible by sea, which was important for the newly formed nation.\n\n**Change of Capital: From Karachi to Islamabad**\n\nThe capital was eventually moved from Karachi to **Rawalpindi (as an interim capital)** and then to the newly constructed city of **Islamabad**.\n\n**When did it happen?**\n\n*   **1959:** The decision to build a new capital, Islamabad, was made by President Ayub Khan\'s government.\n*   **1960:** Construction of Islamabad began.\n*   **1960:** Rawalpindi was designated as the **interim capital** while Islamabad was being built.\n*   **1967:** Islamabad officially became the capital of Pakistan.\n\n**Why the capital was changed from Karachi to Islamabad:**\n\nThe decision to move the capital was driven by several key factors:\n\n1.  **Strategic Location:**\n    *   **Proximity to Military Headquarters:** Rawalpindi, located very close to the eventual site of Islamabad, was already the headquarters of the Pakistan Army. This provided a strategic advantage for national security and defense coordination.\n    *   **More Central Location:** Karachi is located at the southern tip of Pakistan. Moving the capital northward to Islamabad provided a more central location within the country, making it more accessible to people from all provinces, especially those from Punjab and Khyber Pakhtunkhwa.\n    *   **Away from Coastal Vulnerability:** A coastal capital like Karachi was considered vulnerable to sea attacks in times of conflict.\n\n2.  **Climate and Environment:**\n    *   **Better Climate:** Karachi\'s hot and humid climate was often considered uncomfortable for a capital city, especially for administrative work. Islamabad, nestled in the foot of the Margalla Hills, offered a much more pleasant and cooler climate.\n    *   **Clean and Green Environment:** The planning for Islamabad aimed for a clean, green, and aesthetically pleasing city, distinct from the bustling and often crowded atmosphere of Karachi.\n\n3.  **To Foster National Unity and Identity:**\n    *   **Symbol of a New Nation:** A purpose-built capital was seen as a powerful symbol of a new, independent nation, free from colonial legacies and existing regional power structures. It was intended to represent the aspirations of all Pakistanis.\n    *   **Avoid Regional Dominance:** Karachi was a major economic center and the capital of Sindh province. Some feared that its continued status as capital might lead to a perception of dominance by one province over others. Building a new capital in a relatively neutral territory was an attempt to mitigate this.\n\n4.  **Security and Governance:**\n    *   **Orderly Development:** A new capital could be planned and developed systematically, allowing for well-organized government buildings, residential areas, and infrastructure, which was difficult to achieve in an already sprawling city like Karachi.\n    *   **Reduced Urban Congestion:** Moving the administrative functions out of Karachi helped ease the immense pressure on its infrastructure and population, allowing it to focus on its role as a commercial and industrial hub.\n\nIn summary, while Karachi served as Pakistan\'s capital from day one, the strategic, climatic, and national identity considerations led to the planned development of Islamabad as the new and current capital of Pakistan.', '2026-06-26 05:02:38');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password_hash` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `name`, `email`, `password_hash`) VALUES
(5, 'asad', 'asad@gmail.com', '$2b$12$2DHrB0Agr4coYFsWpL8cXOnJZvkBGNGa1l7WyAMvbyfkC1l/XBmgm'),
(6, 'haseeb', 'mohdhaseb2004@gmail.com', '$2b$12$7l7y3RN//lYJFFWZbLFcE.N6zZ3YsSwqZcF9pZ1dwoQLxp5eYlJ26');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`category_id`),
  ADD UNIQUE KEY `category_name` (`category_name`);

--
-- Indexes for table `favorites`
--
ALTER TABLE `favorites`
  ADD PRIMARY KEY (`favorite_id`),
  ADD UNIQUE KEY `unique_user_favorite` (`user_id`,`prompt_id`),
  ADD KEY `prompt_id` (`prompt_id`);

--
-- Indexes for table `models`
--
ALTER TABLE `models`
  ADD PRIMARY KEY (`model_id`);

--
-- Indexes for table `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`project_id`),
  ADD KEY `category_id` (`category_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `project_prompts`
--
ALTER TABLE `project_prompts`
  ADD PRIMARY KEY (`project_prompt_id`),
  ADD UNIQUE KEY `project_id` (`project_id`,`prompt_id`),
  ADD KEY `prompt_id` (`prompt_id`);

--
-- Indexes for table `prompts`
--
ALTER TABLE `prompts`
  ADD PRIMARY KEY (`prompt_id`),
  ADD KEY `category_id` (`category_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `prompt_executions`
--
ALTER TABLE `prompt_executions`
  ADD PRIMARY KEY (`execution_id`),
  ADD KEY `prompt_id` (`prompt_id`),
  ADD KEY `model_id` (`model_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `favorites`
--
ALTER TABLE `favorites`
  MODIFY `favorite_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `projects`
--
ALTER TABLE `projects`
  MODIFY `project_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `project_prompts`
--
ALTER TABLE `project_prompts`
  MODIFY `project_prompt_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `prompts`
--
ALTER TABLE `prompts`
  MODIFY `prompt_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `prompt_executions`
--
ALTER TABLE `prompt_executions`
  MODIFY `execution_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `favorites`
--
ALTER TABLE `favorites`
  ADD CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`prompt_id`) REFERENCES `prompts` (`prompt_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `favorites_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `projects`
--
ALTER TABLE `projects`
  ADD CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `projects_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `project_prompts`
--
ALTER TABLE `project_prompts`
  ADD CONSTRAINT `project_prompts_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `project_prompts_ibfk_2` FOREIGN KEY (`prompt_id`) REFERENCES `prompts` (`prompt_id`) ON DELETE CASCADE;

--
-- Constraints for table `prompts`
--
ALTER TABLE `prompts`
  ADD CONSTRAINT `prompts_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `prompts_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `prompt_executions`
--
ALTER TABLE `prompt_executions`
  ADD CONSTRAINT `prompt_executions_ibfk_1` FOREIGN KEY (`prompt_id`) REFERENCES `prompts` (`prompt_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `prompt_executions_ibfk_2` FOREIGN KEY (`model_id`) REFERENCES `models` (`model_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `prompt_executions_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
