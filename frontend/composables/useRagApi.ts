export const useRagApi = () => {
  // @ts-ignore
  const config = useRuntimeConfig();
  const baseUrl = config.public.ragServiceUrl;

  const fetchRagQuery = async (query: string, userId: string) => {
    try {
      // @ts-ignore
      const { getAuthHeader } = useAuth();
      const headers = (await getAuthHeader()) || undefined;

      // @ts-ignore
      const data = await $fetch(`${baseUrl}/rag/query`, {
        method: "POST",
        headers,
        body: {
          query,
          user_id: userId,
          top_k: 10,
        },
      });
      return data;
    } catch (error) {
      console.error("Error fetching RAG query:", error);
      throw error;
    }
  };

  const checkRagHealth = async () => {
    try {
      // @ts-ignore
      const data = await $fetch(`${baseUrl}/health`);
      return data;
    } catch (error) {
      console.error("Error checking RAG health:", error);
      return null;
    }
  };

  return {
    fetchRagQuery,
    checkRagHealth,
  };
};
