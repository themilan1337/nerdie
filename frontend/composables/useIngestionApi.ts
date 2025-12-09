export const useIngestionApi = () => {
  const config = useRuntimeConfig();
  const baseUrl = config.public.ingestionServiceUrl;

  console.log("[useIngestionApi] Initialized with baseUrl:", baseUrl);

  if (!baseUrl) {
    console.error(
      "[useIngestionApi] ERROR: ingestionServiceUrl is not defined in runtime config!"
    );
  }

  const uploadDocument = async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);

    let endpoint = "/ingest/upload"; // Default or legacy
    if (file.type === "application/pdf") {
      endpoint = "/ingest/pdf";
    } else if (file.type.startsWith("image/")) {
      endpoint = "/ingest/image";
    } else if (file.type === "text/plain") {
      // Text endpoint might expect JSON, check API specs.
      // The ingestion.json shows /ingest/text expects JSON with text string.
      // If we have a file, we might need to read it or use a generic upload if available.
      // The swagger shows /ingest/upload as legacy but maybe useful.
      // Let's stick to /ingest/pdf and /ingest/image for now as they are multipart.
      // For text file, we might need to read content and send to /ingest/text or use /ingest/upload if it handles it.
      // Let's use /ingest/upload for others for now if it works, or just restrict to PDF/Image as typically RAG is PDF.
      endpoint = "/ingest/upload";
    }

    try {
      // @ts-ignore
      const { getAuthHeader } = useAuth();
      const headers = getAuthHeader();

      if (!headers) {
        throw new Error("Not authenticated. Please sign in again.");
      }

      // @ts-ignore
      const data = await $fetch(`${baseUrl}${endpoint}`, {
        method: "POST",
        headers,
        body: formData,
        // Add timeout to prevent hanging
        timeout: 120000, // 2 minutes timeout
      });
      return data;
    } catch (error: any) {
      console.error("Error uploading document:", error);

      // Provide more helpful error messages
      if (error?.statusCode === 401 || error?.status === 401) {
        throw new Error("Authentication expired. Please sign in again.");
      } else if (error?.statusCode === 413 || error?.status === 413) {
        throw new Error("File is too large to upload.");
      } else if (error?.statusCode === 415 || error?.status === 415) {
        throw new Error("File type not supported.");
      } else if (error?.statusCode === 500 || error?.status === 500) {
        throw new Error("Server error. Please try again later.");
      } else if (error?.message?.includes("timeout")) {
        throw new Error("Upload timed out. Please try a smaller file.");
      } else if (
        error?.message?.includes("network") ||
        error?.message?.includes("fetch")
      ) {
        throw new Error("Network error. Please check your connection.");
      }

      throw error;
    }
  };

  const fetchDocuments = async () => {
    try {
      // Note: The Swagger shows /ingest/documents returns a list.
      // @ts-ignore
      const { getAuthHeader } = useAuth();
      const headers = getAuthHeader();

      if (!headers) {
        console.warn("No auth headers available for fetching documents");
        return [];
      }

      // @ts-ignore
      const data = await $fetch(`${baseUrl}/ingest/documents`, {
        headers,
        timeout: 30000, // 30 seconds timeout
      });

      // Handle response format: { documents: [...] } or [...]
      if (
        data &&
        typeof data === "object" &&
        "documents" in data &&
        Array.isArray((data as any).documents)
      ) {
        return (data as any).documents;
      }

      return (data as any[]) || [];
    } catch (error: any) {
      console.error("Error fetching documents:", error);

      // Provide more helpful error messages
      if (error?.statusCode === 401 || error?.status === 401) {
        throw new Error("Authentication expired. Please sign in again.");
      } else if (error?.statusCode === 500 || error?.status === 500) {
        throw new Error("Server error while fetching documents.");
      } else if (error?.message?.includes("timeout")) {
        throw new Error("Request timed out. Please try again.");
      } else if (
        error?.message?.includes("network") ||
        error?.message?.includes("fetch")
      ) {
        throw new Error("Network error. Please check your connection.");
      }

      // Return empty array on error but log it
      console.warn("Returning empty documents array due to error");
      return [];
    }
  };

  return {
    uploadDocument,
    fetchDocuments,
  };
};
